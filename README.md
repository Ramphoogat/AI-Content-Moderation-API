# AI Content Moderation API

A production-ready, high-performance API for filtering text content using a hybrid approach (Rule-based + AI).

## Features

- **Hybrid Analysis**: Combines instant regex/keyword rules with OpenAI's moderation model.
- **Privacy First**: Logs only content hashes, not the raw content.
- **Configurable Strictness**: Low, Medium, High sensitivity presets.
- **Detailed Scoring**: Returns scores for Hate, Harassment, Sexual, Self-harm, Violence, and Spam.
- **Production Ready**: Async SQLAlchemy, Docker, Redis caching hook, and Pydantic validation.

## Tech Stack

- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL (Asyncpg)
- **AI**: OpenAI API (Fallback to local dummy if key missing)
- **Container**: Docker + Docker Compose

## Quick Start

### 1. Run with Docker (Recommended)

```bash
# 1. Create .env file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 2. Start services
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

### 2. Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start DB (Ensure Postgres is running or use Docker for just DB)
docker-compose up -d db redis

# Run App
uvicorn app.main:app --reload
```

## API Usage

### Authentication
Include header `x-api-key: test-key-123` (Default dev key).

### Moderate Text

`POST /api/v1/moderate/text`

**Request:**
```json
{
  "content": "I hate you so much!",
  "strictness": "high",
  "return_spans": true
}
```

**Response:**
```json
{
  "allowed": false,
  "risk_score": 95.5,
  "categories": {
    "hate": 0.99,
    "harassment": 0.4,
    ...
  },
  "flagged_phrases": ["hate"],
  "explanation": "Content flagged due to high risk score."
}
```

### Metrics (Admin)

`GET /api/v1/admin/metrics`

## Pricing Model (Suggestion)

- **Free Tier**: 1k req/month (Rule-based only)
- **Pro Tier**: $29/mo (50k req/month, AI analysis)
- **Enterprise**: Custom volume, dedicated instance, custom logic.

## Project Structure

- `app/api`: Routes and endpoints.
- `app/core`: Configuration and Security.
- `app/services`: Logic (AI, Rules, Normalization).
- `app/models`: Database schemas.

## Python SDK Example

```python
import requests

def match_content(text, api_key="test-key-123"):
    url = "http://localhost:8000/api/v1/moderate/text"
    headers = {"x-api-key": api_key}
    payload = {
        "content": text,
        "strictness": "medium"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

print(match_content("Hello world"))
```
