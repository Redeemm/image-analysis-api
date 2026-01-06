from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Endpoints that don't require authentication
PUBLIC_ENDPOINTS = ["/", "/health", "/api/v1/docs", "/api/v1/redoc", "/api/v1/openapi.json"]


class APIKeyMiddleware(BaseHTTPMiddleware):
    """Middleware for API key authentication"""

    async def dispatch(self, request: Request, call_next):
        """Validate API key for protected endpoints"""

        # Allow public endpoints
        if request.url.path in PUBLIC_ENDPOINTS:
            return await call_next(request)

        # Get API key from header
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            logger.warning(f"Missing API key for {request.url.path}")
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing API key. Include X-API-Key header."}
            )

        # Validate API key
        if api_key != settings.api_key:
            logger.warning(f"Invalid API key attempt for {request.url.path}")
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid API key"}
            )

        logger.debug(f"API key validated for {request.url.path}")
        return await call_next(request)
