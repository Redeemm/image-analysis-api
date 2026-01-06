# Image Analysis API

A FastAPI-based backend service for mobile image upload and analysis.

## Features

- Image upload endpoint with validation (JPEG/PNG, max 5MB)
- Mock image analysis with detailed structured JSON responses
- API key authentication for endpoint security
- Structured logging with correlation IDs for request tracing
- Standardized error responses with error codes
- API versioning (`/api/v1/`)
- Pydantic models for type-safe request/response validation
- Environment-based configuration
- Comprehensive unit and integration test suite
- Clean separation of concerns (routes, services, utilities, models)
- CORS support for mobile app integration
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

4. **Configure environment (required):**
   ```bash
   cp .env.example .env
   # Edit .env if you need to change any settings
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

## Authentication

All API endpoints (except `/` and `/health`) require API key authentication.

Include the API key in the `X-API-Key` header:

```bash
X-API-Key: your-secret-api-key-here
```

Set your API key in the `.env` file:
```
API_KEY=your-secret-api-key-here
```

## Available Endpoints

### Health Check

**GET /**

Returns service status and version information. No authentication required.

```bash
curl http://localhost:8000/
```

### Upload Image

**POST /api/v1/upload**

Upload an image for analysis. Requires authentication.

**Request:**
- Headers: `X-API-Key`
- Content-Type: `multipart/form-data`
- Body: `file` (JPEG or PNG, max 5MB)

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -H "X-API-Key: your-secret-api-key-here" \
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

Analyze a previously uploaded image. Requires authentication.

**Request:**
- Headers: `X-API-Key`, `Content-Type: application/json`
- Body:
```json
{
  "image_id": "abc123-def456-ghi789"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "X-API-Key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{"image_id":"abc123-def456-ghi789"}'
```

**Response (200):**
```json
{
  "success": true,
  "image_id": "abc123-def456-ghi789",
  "timestamp": "2026-01-06T14:05:22Z",
  "image_metadata": {
    "format": "jpeg",
    "width": 1080,
    "height": 1080,
    "file_size_kb": 842.5,
    "color_space": "RGB"
  },
  "analysis": {
    "skin_type": {
      "value": "Oily",
      "confidence": 0.92
    },
    "issues": [
      {
        "name": "Hyperpigmentation",
        "severity": "Medium",
        "confidence": 0.85
      },
      {
        "name": "Acne",
        "severity": "High",
        "confidence": 0.90
      }
    ],
    "confidence": 0.87,
    "analysis_notes": "Detected Category A with 2 issue(s)."
  }
}
```

### Error Responses

All error responses follow a standardized format:

```json
{
  "success": false,
  "timestamp": "2026-01-06T14:05:22Z",
  "error": {
    "code": "ERROR_CODE",
    "message": "Detailed error message",
    "field": "field_name"
  },
  "correlation_id": "abc123-def456"
}
```

**Common Error Codes:**

- `AUTHENTICATION_ERROR`: Missing or invalid API key (401)
- `VALIDATION_ERROR`: Request validation failed (400/422)
- `FILE_VALIDATION_ERROR`: File upload validation failed (400)
- `RESOURCE_NOT_FOUND`: Requested resource not found (404)
- `INTERNAL_SERVER_ERROR`: Unexpected server error (500)

**Example Error:**
```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@large_image.jpg"

# Response (401):
{
  "success": false,
  "timestamp": "2026-01-06T14:05:22Z",
  "error": {
    "code": "AUTHENTICATION_ERROR",
    "message": "Missing API key. Include X-API-Key header."
  },
  "correlation_id": "f8e3a123-45b6-78c9"
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
│   │   ├── logging.py              # Request logging middleware
│   │   └── authentication.py       # API key authentication
│   └── utils/
│       ├── validators.py           # Validation utilities
│       ├── logger.py               # Structured logging
│       ├── exceptions.py           # Custom exceptions
│       └── error_handlers.py       # Global error handlers
├── tests/
│   ├── conftest.py                  # Pytest fixtures
│   ├── test_services.py             # Unit tests
│   └── test_api.py                  # Integration tests
├── uploads/                         # Image storage directory
├── .env.example                     # Environment configuration template
├── pytest.ini                       # Pytest configuration
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Container configuration
└── README.md
```

## Configuration

All configuration is loaded from the `.env` file (required). Copy `.env.example` to `.env` and modify as needed.

Key settings:
- `APP_NAME`: Application name
- `APP_VERSION`: Application version
- `ENVIRONMENT`: Environment (development, staging, production)
- `API_V1_PREFIX`: API version prefix
- `API_KEY`: API key for authentication
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `MAX_FILE_SIZE`: Maximum upload size in bytes
- `UPLOAD_DIR`: Image storage directory
- `ALLOWED_EXTENSIONS`: Allowed MIME types for uploads
- `ALLOWED_FILE_EXTENSIONS`: Allowed file extensions

## Testing

The project includes comprehensive unit and integration tests using pytest.

### Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run with verbose output
pytest -v
```

### Test Structure

```
tests/
├── conftest.py           # Pytest fixtures and configuration
├── test_services.py      # Unit tests for services
└── test_api.py          # Integration tests for API endpoints
```

### Test Coverage

- **Unit Tests**: Services (image_service, analysis_service)
- **Integration Tests**: API endpoints (upload, analyze, authentication)
- **Error Handling**: Validation errors, authentication errors, not found errors

### Example Workflow

```bash
# Start the server
uvicorn app.main:app --reload

# Upload an image with API key
IMAGE_ID=$(curl -X POST "http://localhost:8000/api/v1/upload" \
  -H "X-API-Key: your-secret-api-key-here" \
  -F "file=@test_image.jpg" | jq -r '.image_id')

# Analyze the image
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "X-API-Key: your-secret-api-key-here" \
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
