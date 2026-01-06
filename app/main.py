from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import upload, analyze
from app.config import settings
from app.middleware.logging import LoggingMiddleware
from app.middleware.authentication import APIKeyMiddleware
from app.utils.logger import setup_logging, get_logger
from app.models.responses import HealthCheckResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger = get_logger(__name__)
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Log level: {settings.log_level}")
    yield
    # Shutdown
    logger.info("Shutting down application")


setup_logging(settings.log_level)


app = FastAPI(
    title=settings.app_name,
    description="Backend service for mobile image upload and AI-powered skin analysis",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url=f"{settings.api_v1_prefix}/docs",
    redoc_url=f"{settings.api_v1_prefix}/redoc",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    swagger_ui_parameters={
        "persistAuthorization": True  # Persist API key across page refreshes
    }
)

# Add API Key security scheme for Swagger UI
app.openapi_schema = None  # Reset schema to regenerate with security


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    from fastapi.openapi.utils import get_openapi

    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.app_version,
        description="Backend service for mobile image upload and AI-powered skin analysis",
        routes=app.routes,
    )

    # Add API Key security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "APIKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "API Key for authentication. Get your API key from the .env file."
        }
    }

    # Apply security globally to all endpoints except public ones
    for path, path_item in openapi_schema["paths"].items():
        if path not in ["/", "/health"]:
            for method in path_item.values():
                if isinstance(method, dict) and "operationId" in method:
                    method["security"] = [{"APIKeyHeader": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.add_middleware(LoggingMiddleware)
app.add_middleware(APIKeyMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 routers with versioning
app.include_router(
    upload.router,
    prefix=settings.api_v1_prefix,
    tags=["upload"]
)
app.include_router(
    analyze.router,
    prefix=settings.api_v1_prefix,
    tags=["analyze"]
)


@app.get("/", response_model=HealthCheckResponse, tags=["health"])
async def root():
    return HealthCheckResponse(
        status="running",
        service=settings.app_name,
        version=settings.app_version
    )


@app.get("/health", response_model=HealthCheckResponse, tags=["health"])
async def health_check():
    return HealthCheckResponse(
        status="healthy",
        service=settings.app_name,
        version=settings.app_version
    )
