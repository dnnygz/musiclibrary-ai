# MusicLibrary AI API

AI-powered microservice for the MusicLibrary system. Provides intelligent features like playlist descriptions, song recommendations, mood analysis, and semantic search using Groq AI.

## Features

- **Playlist Descriptions**: Generate creative, engaging descriptions for playlists
- **Song Recommendations**: Get AI-powered song suggestions based on playlist content
- **Playlist Naming**: Generate creative names in different styles (creative, descriptive, fun)
- **Mood Analysis**: Analyze the emotional character and mood of playlists
- **Semantic Search**: Search for songs using natural language descriptions

## Tech Stack

- **Framework**: FastAPI
- **AI Model**: Groq (llama-3.3-70b-versatile)
- **Language**: Python 3.11+
- **Validation**: Pydantic v2

## Prerequisites

- Python 3.11, 3.12, or 3.13
- Groq API key (get it at https://console.groq.com)

**Note**: If you're using Python 3.13, make sure you have the latest versions of dependencies installed. If you encounter build errors with `pydantic-core`, try using Python 3.11 or 3.12 instead.

## Setup

1. **Clone the repository**

```bash
cd musiclibrary-ai
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

5. **Run the server**

```bash
# Development
uvicorn app.main:app --reload --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:

- **Swagger UI**: `http://localhost:8000/docs` - Interactive API documentation
- **ReDoc**: `http://localhost:8000/redoc` - Alternative API documentation

All endpoints are documented with request/response schemas and examples.

## Docker

Build and run with Docker:

```bash
docker build -t musiclibrary-ai .
docker run -p 8000:8000 --env-file .env musiclibrary-ai
```

## Example Usage

### Describe Playlist

```bash
curl -X POST "http://localhost:8000/describe-playlist" \
  -H "Content-Type: application/json" \
  -d '{
    "songs": [
      {
        "id": "1",
        "title": "Bohemian Rhapsody",
        "artist": "Queen",
        "genre": "Rock",
        "year": 1975,
        "duration": 354
      }
    ]
  }'
```

### Get Recommendations

```bash
curl -X POST "http://localhost:8000/recommend-songs" \
  -H "Content-Type: application/json" \
  -d '{
    "current_songs": [
      {
        "id": "1",
        "title": "Bohemian Rhapsody",
        "artist": "Queen",
        "genre": "Rock",
        "year": 1975,
        "duration": 354
      }
    ],
    "number_of_recommendations": 5
  }'
```

### Generate Playlist Names

```bash
curl -X POST "http://localhost:8000/generate-name" \
  -H "Content-Type: application/json" \
  -d '{
    "songs": [
      {
        "id": "1",
        "title": "Bohemian Rhapsody",
        "artist": "Queen",
        "genre": "Rock",
        "year": 1975,
        "duration": 354
      }
    ],
    "style": "creative"
  }'
```

### Analyze Mood

```bash
curl -X POST "http://localhost:8000/analyze-mood" \
  -H "Content-Type: application/json" \
  -d '{
    "songs": [
      {
        "id": "1",
        "title": "Bohemian Rhapsody",
        "artist": "Queen",
        "genre": "Rock",
        "year": 1975,
        "duration": 354
      }
    ]
  }'
```

### Semantic Search

```bash
curl -X POST "http://localhost:8000/semantic-search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "upbeat songs for running in the morning",
    "limit": 10
  }'
```

## Project Structure

```
app/
├── main.py                    # FastAPI application entry point
├── config.py                  # Configuration and environment variables
├── models/                     # Pydantic models
│   ├── song.py                # Song model
│   ├── requests.py            # Request models
│   └── responses.py           # Response models
├── services/                   # Business logic
│   ├── groq_service.py        # Groq API integration
│   └── ai_service.py          # AI feature business logic
├── routers/                    # API routes
│   └── ai_routes.py           # AI endpoint handlers
├── prompts/                    # AI prompts
│   ├── describe_playlist.py   # Playlist description prompts
│   ├── recommend_songs.py     # Recommendation prompts
│   ├── generate_name.py       # Name generation prompts
│   ├── analyze_mood.py        # Mood analysis prompts
│   └── semantic_search.py    # Semantic search prompts
└── utils/                      # Utilities
    ├── exceptions.py          # Custom exceptions
    ├── helpers.py            # Helper functions
    └── logger.py             # Logging configuration
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `8000` |
| `ENVIRONMENT` | Environment mode | `development` |
| `GROQ_API_KEY` | Groq API key | Required |
| `GROQ_MODEL` | Groq model to use | `llama-3.3-70b-versatile` |
| `GROQ_MAX_TOKENS` | Maximum tokens per request | `2000` |
| `ALLOWED_ORIGINS` | CORS origins (comma-separated) | `http://localhost:3001,http://localhost:3000` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Error Handling

The API returns structured error responses:

```json
{
  "detail": "Error message",
  "error_type": "error_category"
}
```

Error types:

- `validation_error`: Request validation failed
- `ai_service_error`: AI service error
- `rate_limit_error`: Rate limit exceeded
- `internal_error`: Internal server error

## Testing Connection

### Quick Test Script

We provide a Python test script to verify the API is working:

```bash
python test_connection.py
```

The script tests all endpoints and provides detailed output.

### Manual Testing with curl

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Describe Playlist:**
```bash
curl -X POST "http://localhost:8000/describe-playlist" \
  -H "Content-Type: application/json" \
  -d '{
    "songs": [{
      "id": "1",
      "title": "Bohemian Rhapsody",
      "artist": "Queen",
      "genre": "Rock",
      "year": 1975,
      "duration": 354
    }]
  }'
```

**Note:** Make sure you have `requests` installed for the test script:
```bash
pip install requests
```

## License

MIT

