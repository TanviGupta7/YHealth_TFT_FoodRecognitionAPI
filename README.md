# YHealth by TFT

AI-Powered Food and Nutrition Analyzer — upload a photo, get calories and macros instantly.

## Features

- Upload or camera capture (JPEG, PNG, WEBP)
- Local ViT classifier (`nateraw/food`, Food-101) — works without API key
- Optional HuggingFace router API fallback (`INFERENCE_MODE=auto|hf`)
- Nutrition mapping for all 101 Food-101 classes + Indian/extra foods
- Dark Streamlit UI with macro cards and JSON API
- Docker Compose one-command deploy

## Quick Start (Docker)

```bash
cd food-ai
cp .env.example .env
docker compose up --build
```

- **Frontend:** http://localhost:8501  
- **API docs:** http://localhost:8000/docs  

First backend start may take 1–2 minutes while the model loads.

## Local Dev (no Docker)

**Backend**
```bash
cd backend
pip install -r requirements.txt
set INFERENCE_MODE=local
uvicorn main:app --reload --port 8000
```

**Frontend**
```bash
cd frontend
pip install -r requirements.txt
set API_URL=http://localhost:8000
streamlit run app.py
```

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `INFERENCE_MODE` | `local` | `local`, `hf`, or `auto` |
| `HF_API_KEY` | — | Optional HF token for remote inference |
| `API_URL` | `http://localhost:8000` | Backend URL for Streamlit |
| `RATE_LIMIT` | `20` | Requests per IP per minute |

## API

### `POST /analyze`

Multipart form field `file` (image).

### `GET /health`

Returns model load status.

## Deploy

### Render

Push to GitHub, connect repo, use `render.yaml` blueprint (two web services).

Set `API_URL` on the frontend service to the backend public URL if not auto-linked.

### Railway

Deploy **two services** from the same repo:

1. **Backend** — root `railway.toml`, Dockerfile `backend/Dockerfile`
2. **Frontend** — `frontend/railway.toml`, set `API_URL` to backend public URL

## Architecture

```
food-ai/
├── backend/
│   ├── main.py           # FastAPI routes
│   ├── inference.py      # Local + HF classification
│   ├── nutrition_data.py # Macro database
│   └── Dockerfile
├── frontend/
│   └── app.py            # Streamlit UI
└── docker-compose.yml
```

Built with FastAPI · Streamlit · HuggingFace Transformers
