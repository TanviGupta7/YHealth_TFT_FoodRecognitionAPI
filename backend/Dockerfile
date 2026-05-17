FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    TRANSFORMERS_CACHE=/app/.cache/huggingface \
    HF_HOME=/app/.cache/huggingface \
    INFERENCE_MODE=local

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY nutrition_data.py inference.py security.py middleware.py meal_logic.py main.py .

# Pre-download model so first request is fast
RUN python -c "from transformers import pipeline; pipeline('image-classification', model='nateraw/food', device=-1)"

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
