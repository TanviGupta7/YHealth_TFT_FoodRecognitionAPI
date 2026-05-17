import logging
import os
import time
from collections import defaultdict
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from inference import HF_MODEL, classify_food
from middleware import SecurityHeadersMiddleware
from nutrition_data import calculate_total_macros, get_nutrition, resolve_food
from security import validate_image_upload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

request_times = defaultdict(list)
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "20"))
MAX_FILE_BYTES = int(os.getenv("MAX_FILE_BYTES", str(10 * 1024 * 1024)))
MAX_ITEMS = int(os.getenv("MAX_ITEMS", "3"))
MIN_ITEM_CONFIDENCE = float(os.getenv("MIN_ITEM_CONFIDENCE", "0.15"))
ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")


@asynccontextmanager
async def lifespan(app: FastAPI):
    mode = os.getenv("INFERENCE_MODE", "local")
    if mode in ("local", "auto"):
        from inference import _load_local_classifier

        _load_local_classifier()
    yield


app = FastAPI(
    title="YHealth by TFT API",
    description="AI-Powered Food and Nutrition Analyzer",
    version="2.0.0",
    lifespan=lifespan,
)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred. Please try again."},
    )


def check_rate_limit(client_ip: str):
    now = time.time()
    request_times[client_ip] = [t for t in request_times[client_ip] if now - t < 60]
    if len(request_times[client_ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again in a minute.",
        )
    request_times[client_ip].append(now)


def build_items(predictions: list[dict]) -> tuple[list[dict], list[dict]]:
    api_items: list[dict] = []
    confidence_meta: list[dict] = []
    seen_names: set[str] = set()

    for idx, pred in enumerate(predictions):
        score = float(pred["score"])
        if idx > 0 and score < MIN_ITEM_CONFIDENCE:
            continue

        label = pred["label"]
        _, display_name = resolve_food(label)
        if display_name.lower() in seen_names:
            continue
        seen_names.add(display_name.lower())

        nutrition = get_nutrition(label)
        confidence = round(score * 100, 1)

        api_items.append(
            {
                "name": display_name,
                "quantity": nutrition.get("quantity", "1 serving"),
                "calories": int(nutrition["calories"]),
                "protein_g": nutrition["protein_g"],
                "carbs_g": nutrition["carbs_g"],
                "fat_g": nutrition["fat_g"],
            }
        )
        confidence_meta.append({"name": display_name, "confidence": confidence})

        if len(api_items) >= MAX_ITEMS:
            break

    return api_items, confidence_meta


@app.get("/")
def root():
    return {"status": "ok", "app": "YHealth by TFT", "message": "Nutrition API is running"}


@app.get("/health")
def health():
    from inference import _classifier, _classifier_error

    return {
        "status": "healthy",
        "app": "YHealth by TFT",
        "model": HF_MODEL,
        "inference_mode": os.getenv("INFERENCE_MODE", "local"),
        "local_model_loaded": _classifier is not None,
        "local_model_error": _classifier_error,
    }


@app.post("/analyze")
async def analyze_food(request: Request, file: UploadFile = File(...)):
    client_ip = request.client.host if request.client else "unknown"
    check_rate_limit(client_ip)

    contents = await file.read()
    validate_image_upload(
        contents,
        file.filename or "upload.jpg",
        file.content_type or "",
        MAX_FILE_BYTES,
    )

    try:
        predictions = classify_food(contents)
        items, confidence_meta = build_items(predictions)
    except RuntimeError as exc:
        logger.error("Inference failed: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="Food recognition is temporarily unavailable. Please try again.",
        )

    if not items:
        raise HTTPException(
            status_code=422,
            detail="No food items detected with sufficient confidence.",
        )

    return {
        "items": items,
        "total_macros": calculate_total_macros(items),
        "confidence_scores": confidence_meta,
    }
