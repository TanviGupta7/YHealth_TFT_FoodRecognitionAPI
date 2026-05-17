import io
import logging
from typing import Tuple

from fastapi import HTTPException
from PIL import Image

logger = logging.getLogger(__name__)

ALLOWED_MIME = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}

# JPEG / PNG / WEBP magic-byte prefixes
SIGNATURES = (
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"\x89PNG\r\n\x1a\n", "image/png"),
    (b"RIFF", "image/webp"),  # WEBP: RIFF....WEBP checked below
)


def _detect_mime(header: bytes) -> str | None:
    if header.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if header[:4] == b"RIFF" and len(header) >= 12 and header[8:12] == b"WEBP":
        return "image/webp"
    return None


def validate_image_upload(
    contents: bytes,
    filename: str,
    content_type: str,
    max_bytes: int,
) -> bytes:
    if len(contents) < 100:
        raise HTTPException(status_code=400, detail="File is empty or too small.")
    if len(contents) > max_bytes:
        mb = max_bytes // (1024 * 1024)
        raise HTTPException(status_code=400, detail=f"File too large. Max {mb}MB.")

    ext = ""
    if filename and "." in filename:
        ext = "." + filename.rsplit(".", 1)[-1].lower()
    if ext and ext not in ALLOWED_EXT:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG, PNG, and WEBP images are allowed.",
        )

    declared = (content_type or "").lower().split(";")[0].strip()
    if declared and declared not in ALLOWED_MIME:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG, PNG, and WEBP images are allowed.",
        )

    detected = _detect_mime(contents[:16])
    if not detected:
        raise HTTPException(status_code=400, detail="Invalid image file type.")

    if declared and declared != detected and declared.replace("image/jpg", "image/jpeg") != detected:
        logger.warning("MIME mismatch: declared=%s detected=%s", declared, detected)

    try:
        img = Image.open(io.BytesIO(contents))
        img.verify()
        img = Image.open(io.BytesIO(contents))
        img.convert("RGB")
        if img.size[0] < 32 or img.size[1] < 32:
            raise HTTPException(status_code=400, detail="Image resolution is too small.")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or corrupted image.")

    return contents
