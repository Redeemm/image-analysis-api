from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import upload, analyze
from app.config import settings
from app.middleware.logging import LoggingMiddleware
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
)


app.add_middleware(LoggingMiddleware)


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
