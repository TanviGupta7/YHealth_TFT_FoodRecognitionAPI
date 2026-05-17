import io
import logging
import os
import time
from typing import Optional

import requests
from PIL import Image

logger = logging.getLogger(__name__)

HF_API_KEY = os.getenv("HF_API_KEY", "")
HF_MODEL = os.getenv("HF_MODEL", "nateraw/food")
INFERENCE_MODE = os.getenv("INFERENCE_MODE", "local").lower()  # local | hf | auto
MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", "0.05"))
TOP_K = int(os.getenv("TOP_K", "8"))

HF_ROUTER_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"

_classifier = None
_classifier_error: Optional[str] = None


def _load_local_classifier():
    global _classifier, _classifier_error
    if _classifier is not None or _classifier_error is not None:
        return
    try:
        from transformers import pipeline

        logger.info("Loading local food classifier (%s)...", HF_MODEL)
        _classifier = pipeline(
            "image-classification",
            model=HF_MODEL,
            device=-1,
        )
        logger.info("Local classifier ready.")
    except Exception as exc:
        _classifier_error = str(exc)
        logger.error("Failed to load local classifier: %s", exc)


def classify_local(image_bytes: bytes) -> list[dict]:
    _load_local_classifier()
    if _classifier is None:
        raise RuntimeError(_classifier_error or "Local classifier unavailable")

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    results = _classifier(image, top_k=TOP_K)
    items = []
    for r in results:
        score = float(r.get("score", 0))
        if score < MIN_CONFIDENCE:
            continue
        label = r["label"]
        items.append({"label": label, "score": score})
    return items


def classify_hf_api(image_bytes: bytes) -> list[dict]:
    headers = {}
    if HF_API_KEY:
        headers["Authorization"] = f"Bearer {HF_API_KEY}"

    for attempt in range(3):
        resp = requests.post(
            HF_ROUTER_URL,
            headers=headers,
            data=image_bytes,
            timeout=45,
        )
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, dict) and "error" in data:
                raise RuntimeError(data["error"])
            items = []
            for r in data:
                score = float(r.get("score", 0))
                if score < MIN_CONFIDENCE:
                    continue
                items.append({"label": r["label"], "score": score})
            return items[:TOP_K]

        if resp.status_code in (503, 504):
            wait = 2 ** attempt
            logger.warning("HF model loading (503), retry in %ss", wait)
            time.sleep(wait)
            continue

        detail = resp.text[:300]
        raise RuntimeError(f"HuggingFace API error {resp.status_code}: {detail}")

    raise RuntimeError("HuggingFace API unavailable after retries")


def classify_food(image_bytes: bytes) -> list[dict]:
    mode = INFERENCE_MODE
    errors = []

    if mode in ("local", "auto"):
        try:
            items = classify_local(image_bytes)
            if items:
                return items
        except Exception as exc:
            errors.append(f"local: {exc}")
            logger.warning("Local inference failed: %s", exc)
        if mode == "local":
            raise RuntimeError(errors[-1] if errors else "No predictions from local model")

    if mode in ("hf", "auto"):
        try:
            items = classify_hf_api(image_bytes)
            if items:
                return items
        except Exception as exc:
            errors.append(f"hf: {exc}")
            logger.warning("HF API inference failed: %s", exc)

    msg = "; ".join(errors) if errors else "No food items detected"
    raise RuntimeError(msg)
