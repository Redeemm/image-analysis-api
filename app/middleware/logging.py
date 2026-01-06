import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger import correlation_id, get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging with correlation IDs"""

    async def dispatch(self, request: Request, call_next):
        # Generate correlation ID
        corr_id = str(uuid.uuid4())
        correlation_id.set(corr_id)

        # Add to response headers
        start_time = time.time()

        # Log incoming request
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={
                'extra_fields': {
                    'correlation_id': corr_id,
                    'method': request.method,
                    'path': request.url.path,
                    'query_params': str(request.query_params),
                    'client_ip': request.client.host if request.client else None,
                }
            }
        )

        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            # Add custom headers
            response.headers['X-Correlation-ID'] = corr_id
            response.headers['X-Process-Time'] = str(process_time)

            # Log response
            logger.info(
                f"Request completed: {request.method} {request.url.path}",
                extra={
                    'extra_fields': {
                        'correlation_id': corr_id,
                        'method': request.method,
                        'path': request.url.path,
                        'status_code': response.status_code,
                        'process_time': f"{process_time:.4f}s",
                    }
                }
            )

            return response

        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Request failed: {request.method} {request.url.path}",
                extra={
                    'extra_fields': {
                        'correlation_id': corr_id,
                        'method': request.method,
                        'path': request.url.path,
                        'error': str(e),
                        'process_time': f"{process_time:.4f}s",
                    }
                },
                exc_info=True
            )
            raise
