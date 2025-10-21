"""
Custom middleware for the application.
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all incoming requests and their processing time.
    """

    async def dispatch(self, request: Request, call_next):
        # Start timer
        start_time = time.time()

        # Get client info
        client_host = request.client.host if request.client else "unknown"

        # Log request
        logger.info(f"Request: {request.method} {request.url.path} from {client_host}")

        # Process request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"- Status: {response.status_code} "
            f"- Time: {process_time:.3f}s"
        )

        # Add custom header with processing time
        response.headers["X-Process-Time"] = str(process_time)

        return response
