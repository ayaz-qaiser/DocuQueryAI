"""
DocuQuery AI - API v1 Package

This package contains the version 1 API endpoints and routers.
"""

from .router import api_router
from .health import health_router
from .info import info_router

__all__ = [
    "api_router",
    "health_router",
    "info_router",
]
