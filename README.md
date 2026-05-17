# YHealth

<h1 align="center">YHealth</h1>

<h4 align="center">by Think Future Technologies</h4>

<p align="center">
  Your Food & Nutrition Analyzer
</p>

<p align="center">
  Upload an image of your meal and instantly receive estimated calories, protein, carbs, and fat values.
</p>

---

# Overview

YHealth is a Food Recognition and Nutrition Analysis application designed to identify meals from uploaded food images and estimate nutritional macros such as calories, protein, carbohydrates, and fat.

The project combines:

- HuggingFace Vision Transformer (Food-101)
- FastAPI backend
- Streamlit frontend
- Dockerized deployment
- Lightweight meal heuristics
- Nutrition macro estimation

The goal of the project is to create a practical, demo-friendly nutrition analysis system while maintaining a lightweight and efficient architecture.

---

# Features

- Upload food images
- Camera capture support
- Vision-based food recognition
- Nutrition macro estimation
- Multi-item meal support
- JSON API response
- Streamlit dashboard UI
- Docker deployment
- Lightweight security protections
- Clean and responsive interface

---

# Quick Start

## Docker Setup

```bash
docker compose up --build
```

### Frontend

```text
http://localhost:8501
```

### Backend API

```text
http://localhost:8000/docs
```

---

# Local Development

## Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

# Application Screenshots

## Main Interface

<p align="center">
  <img src="assets/screenshots/paneer%20butter%20masala%20with%20jeera%20rice.png" width="850"/>
</p>

---

## Food Detection Example

<p align="center">
  <img src="assets/screenshots/pizza%20img.jpg" width="650"/>
</p>

---

# Working Demo Images

These sample images can be used to test meal detection and nutrition analysis inside YHealth.

<p align="center">
  <img src="assets/demo_images/d1.png" width="220"/>
  <img src="assets/demo_images/d2.png" width="220"/>
  <img src="assets/demo_images/d3.png" width="220"/>
</p>

<p align="center">
  <img src="assets/demo_images/d4.png" width="220"/>
  <img src="assets/demo_images/d5.png" width="220"/>
  <img src="assets/demo_images/d6.png" width="220"/>
</p>

---

# Demo Video

## Watch Application Demo

[▶ Watch Demo Video](assets/videos/demo_video.mp4)

---

# How It Works

1. User uploads or captures a food image  
2. The image is sent to the FastAPI backend  
3. The HuggingFace ViT model performs food classification  
4. Lightweight meal heuristics improve prediction quality  
5. Nutrition macros are mapped from the nutrition database  
6. Total calories, protein, carbs, and fat are calculated  
7. Results are displayed in the Streamlit dashboard and JSON API response  

---

# Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| Frontend | Streamlit |
| AI Model | HuggingFace ViT (Food-101) |
| Language | Python |
| Containerization | Docker |
| Deployment | Render / Railway |

---

# Security Features

The project includes lightweight security mechanisms suitable for demo and MVP environments.

## Implemented Security Measures

- Upload size limits
- MIME validation
- File type validation
- Pillow image verification
- Lightweight rate limiting
- Security response headers
- Sanitized rendering
- Improved API error handling

---

# Project Structure

```text
food-ai/
├── backend/
│   ├── main.py
│   ├── inference.py
│   ├── meal_logic.py
│   ├── nutrition_data.py
│   ├── security.py
│   └── Dockerfile
│
├── frontend/
│   ├── app.py
│   └── streamlit_compat.py
│
├── assets/
│   ├── screenshots/
│   ├── demo_images/
│   └── videos/
│
├── docker-compose.yml
├── render.yaml
├── railway.toml
└── README.md
```

---

# API Response Example

```json
{
  "items": [
    {
      "name": "Paneer Butter Masala",
      "quantity": "1 bowl",
      "calories": 320,
      "protein_g": 14,
      "carbs_g": 18,
      "fat_g": 22
    },
    {
      "name": "Jeera Rice",
      "quantity": "1 cup",
      "calories": 210,
      "protein_g": 4,
      "carbs_g": 42,
      "fat_g": 3
    }
  ],
  "total_macros": {
    "calories": 530,
    "protein_g": 18,
    "carbs_g": 60,
    "fat_g": 25
  }
}
```

---

# Backend API Documentation

The backend of YHealth is built using FastAPI and provides REST API endpoints for food image analysis, nutrition estimation, health checks, and system communication.

The backend automatically generates interactive API documentation using Swagger UI and ReDoc.

---

# API Documentation URLs

## Swagger UI

```text
http://localhost:8000/docs
```

Interactive API testing interface for developers.

### Features

- Upload food images directly
- Test API endpoints
- View JSON responses
- Inspect request/response schemas
- Debug backend communication

---

## ReDoc Documentation

```text
http://localhost:8000/redoc
```

Clean developer-friendly API reference documentation.

---

# Base URL

```text
http://localhost:8000
```

---

# Available API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/analyze` | Upload food image and receive nutrition analysis |
| GET | `/health` | Check backend and model health status |
| GET | `/docs` | Swagger API documentation |
| GET | `/redoc` | ReDoc API documentation |

---

# POST /analyze

Uploads a food image to the backend for AI-assisted food recognition and nutrition analysis.

## Request Type

```http
POST /analyze
Content-Type: multipart/form-data
```

## Input

| Parameter | Type | Description |
|---|---|---|
| file | Image File | Food image uploaded by user |

### Supported Formats

- JPG
- JPEG
- PNG
- WEBP

---

# Backend Workflow

1. Image validation is performed  
2. Food image is processed using the HuggingFace Food-101 Vision Transformer model  
3. Meal heuristics improve recognition quality  
4. Nutrition values are mapped from the nutrition database  
5. Total calories and macros are calculated  
6. JSON response is returned to the frontend  

---

# GET /health

Checks whether the backend API and AI model are active.

## Request

```http
GET /health
```

## Example Response

```json
{
  "status": "ok",
  "model_loaded": true
}
```

---

# Backend Architecture

| File | Purpose |
|---|---|
| `main.py` | FastAPI routes and API server |
| `inference.py` | Food classification logic |
| `meal_logic.py` | Meal heuristics and post-processing |
| `nutrition_data.py` | Nutrition mapping database |
| `security.py` | Upload validation and security handling |

---

# AI Model Information

| Component | Technology |
|---|---|
| Base Model | HuggingFace Food-101 |
| Framework | Transformers |
| Inference | Python |
| API Framework | FastAPI |

---

# Deployment

## Render

Deploy using:
- `render.yaml`
- Separate frontend and backend services

## Railway

Deploy:
- Backend service
- Frontend service

Set:

```text
API_URL=<backend-public-url>
```

---

# Running Backend Locally

## Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Start Backend Server

```bash
uvicorn main:app --reload --port 8000
```

---

# Backend Access

| Service | URL |
|---|---|
| API Server | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |
| ReDoc Docs | http://localhost:8000/redoc |

---

# Notes

- The backend supports local model inference
- Internet connection is not required for local inference
- Food recognition quality depends on Food-101 model capability
- Lightweight heuristics improve practical meal recognition
- The system is optimized for demonstration and MVP deployment

---

# Built With

- FastAPI
- Streamlit
- HuggingFace Transformers
- Docker
- Python

---

# Developed For

## Think Future Technologies

YHealth — Your Food & Nutrition Analyzer
