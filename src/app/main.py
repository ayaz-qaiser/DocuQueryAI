"""
DocuQuery AI - Main Application Entry Point

This module contains the FastAPI application factory and main configuration.
It wires together all the routers and middleware without implementing business logic.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.timing import TimingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.common.error_handlers import register_error_handlers
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # TODO: Initialize database connections
    # TODO: Initialize Redis connections
    # TODO: Initialize Qdrant connections
    # TODO: Start background workers
    
    yield
    
    # TODO: Close database connections
    # TODO: Close Redis connections
    # TODO: Close Qdrant connections
    # TODO: Stop background workers


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Production-ready AI Document Q&A API",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Add custom middleware
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Include API routers
    app.include_router(api_router, prefix="/api/v1")
    
    # TODO: Add additional feature routers as they are implemented
    # app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    # app.include_router(tenant_router, prefix="/tenants", tags=["Tenants"])
    # app.include_router(user_router, prefix="/users", tags=["Users"])
    # app.include_router(document_router, prefix="/documents", tags=["Documents"])
    # app.include_router(query_router, prefix="/query", tags=["Query"])
    
    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
