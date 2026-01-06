# Image Analysis API

A FastAPI-based backend service for mobile image upload and analysis.

## Features

- Image upload endpoint with validation (JPEG/PNG, max 5MB)
- Mock image analysis with structured JSON responses
- Structured logging with correlation IDs for request tracing
- API versioning (`/api/v1/`)
- Pydantic models for type-safe request/response validation
- Environment-based configuration
- Clean separation of concerns (routes, services, utilities, models)
- CORS support for mobile app integration
- Comprehensive error handling
- Docker support

## Requirements

- Python 3.8+
- pip

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd image-analysis-api
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment (optional):**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Running the Service

Start the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, interactive documentation is available at:
- **Swagger UI:** http://localhost:8000/api/v1/docs
- **ReDoc:** http://localhost:8000/api/v1/redoc

## Available Endpoints

### Health Check

**GET /**

Returns service status and version information.

```bash
curl http://localhost:8000/
```

### Upload Image

**POST /api/v1/upload**

Upload an image for analysis.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (JPEG or PNG, max 5MB)

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@/path/to/image.jpg"
```

**Response (201):**
```json
{
  "success": true,
  "timestamp": "2024-01-06T12:00:00Z",
  "image_id": "abc123-def456-ghi789",
  "message": "Image uploaded successfully",
  "filename": "image.jpg",
  "file_size": 102400
}
```

Response includes headers:
- `X-Correlation-ID`: Unique request identifier
- `X-Process-Time`: Request processing time

### Analyze Image

**POST /api/v1/analyze**

Analyze a previously uploaded image.

**Request:**
```json
{
  "image_id": "abc123-def456-ghi789"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"image_id":"abc123-def456-ghi789"}'
```

**Response (200):**
```json
{
  "success": true,
  "timestamp": "2024-01-06T12:00:00Z",
  "image_id": "abc123-def456-ghi789",
  "skin_type": "Oily",
  "issues": ["Hyperpigmentation", "Acne"],
  "confidence": 0.87,
  "analysis_notes": "Detected oily skin with 2 concern(s)"
}
```

## Project Structure

```
image-analysis-api/
├── app/
│   ├── main.py                      # FastAPI application entry point
│   ├── config.py                    # Environment configuration
│   ├── models/
│   │   ├── requests.py             # Request schemas
│   │   └── responses.py            # Response schemas
│   ├── routes/
│   │   ├── upload.py               # Upload endpoint
│   │   └── analyze.py              # Analysis endpoint
│   ├── services/
│   │   ├── image_service.py        # Image storage logic
│   │   └── analysis_service.py     # Mock analysis logic
│   ├── middleware/
│   │   └── logging.py              # Request logging middleware
│   └── utils/
│       ├── validators.py           # Validation utilities
│       └── logger.py               # Structured logging
├── uploads/                         # Image storage directory
├── .env.example                     # Environment configuration template
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Container configuration
└── README.md
```

## Configuration

Configuration is managed through environment variables or a `.env` file. See `.env.example` for available options.

Key settings:
- `API_V1_PREFIX`: API version prefix (default: `/api/v1`)
- `LOG_LEVEL`: Logging level (default: `INFO`)
- `MAX_FILE_SIZE`: Maximum upload size in bytes (default: 5MB)
- `UPLOAD_DIR`: Image storage directory (default: `uploads`)

## Testing

Example workflow:

```bash
# Start the server
uvicorn app.main:app --reload

# Upload an image
IMAGE_ID=$(curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@test_image.jpg" | jq -r '.image_id')

# Analyze the image
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d "{\"image_id\":\"$IMAGE_ID\"}"
```

## Docker

Build and run with Docker:

```bash
docker build -t image-analysis-api .
docker run -p 8000:8000 image-analysis-api
```

## Assumptions

1. **Mock Analysis**: The analysis endpoint returns simulated results. In production, this would integrate with an actual ML model.

2. **Local Storage**: Images are stored on the local filesystem. Production would use cloud storage (S3, GCS, etc.).

3. **No Authentication**: The API is currently open. Production would require API keys or JWT tokens.

4. **No Database**: Image metadata is not persisted. Production would use a database for tracking uploads, analysis history, and user data.

5. **Deterministic Mock Results**: The mock analysis uses the `image_id` as a seed to provide consistent results for the same image.

## Production Improvements

If this were a production system, I would implement:

**Security:**
- Authentication and authorization (JWT, API keys)
- Rate limiting
- Input sanitization and security headers

**Infrastructure:**
- Cloud storage integration (AWS S3, Google Cloud Storage)
- Database for metadata (PostgreSQL, MongoDB)
- Caching layer (Redis)
- Message queue for async processing (Celery, RabbitMQ)

**Monitoring:**
- Application performance monitoring
- Error tracking (Sentry)
- Centralized logging
- Metrics and alerting

**Testing:**
- Unit tests (pytest)
- Integration tests
- CI/CD pipeline

**Features:**
- Analysis history and user tracking
- Batch processing
- Webhook notifications
- Real ML model integration
