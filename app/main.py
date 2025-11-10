"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.core.config import settings
from app.core.security import initialize_firebase
from app.core.exceptions import (
    validation_exception_handler,
    database_exception_handler,
    general_exception_handler
)
from app.core.middleware import LoggingMiddleware
from app.api.v1 import air_quality, water_quality

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create FastAPI app with custom documentation
app = FastAPI(
    title="Environmental Metrics API",
    description="""
# Environmental Metrics API

This API provides access to environmental quality data including air and water quality metrics.

## Authentication

All endpoints (except `/health`) require Firebase authentication. To use this API:

1. Obtain a Firebase ID token from your authenticated user session
2. Include the token in the `Authorization` header as: `Bearer <your-token>`

Example:
```
Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6...
```

## Available Resources

- **Air Quality**: Access air quality measurements and metrics
- **Water Quality**: Access water quality measurements and metrics

## Rate Limiting

Currently no rate limiting is enforced, but please use the API responsibly.

## Support

For issues or questions, please contact the development team.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    }
)

# Startup event - initialize Firebase
@app.on_event("startup")
async def startup_event():
    """Initialize Firebase on application startup."""
    initialize_firebase()

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Add middleware
app.add_middleware(LoggingMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Root endpoint - redirect to docs
@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to API documentation."""
    return RedirectResponse(url="/docs")

# Health check endpoint (public, no auth required)
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify API is running.

    This endpoint does not require authentication.
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Environmental Metrics API"
    }

# Include API routers
app.include_router(
    air_quality.router,
    prefix="/api/v1/air-quality",
)

app.include_router(
    water_quality.router,
    prefix="/api/v1/water-quality",
)

# API version info endpoint
@app.get("/api/v1", tags=["API Info"])
async def api_info():
    """Get API version and available endpoints information."""
    return {
        "version": "1.0.0",
        "endpoints": {
            "air_quality": "/api/v1/air-quality",
            "water_quality": "/api/v1/water-quality",
            "health": "/health",
            "docs": "/docs"
        }
    }
