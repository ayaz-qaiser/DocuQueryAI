"""
DocuQuery AI - Custom Exceptions

This module defines custom exceptions used throughout the application
for consistent error handling and user feedback.
"""

from typing import Any, Dict, Optional


class DocuQueryException(Exception):
    """Base exception for all DocuQuery AI errors."""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 500
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.status_code = status_code


class AuthenticationError(DocuQueryException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(message, status_code=401, **kwargs)


class AuthorizationError(DocuQueryException):
    """Raised when user lacks required permissions."""
    
    def __init__(self, message: str = "Insufficient permissions", **kwargs):
        super().__init__(message, status_code=403, **kwargs)


class ValidationError(DocuQueryException):
    """Raised when data validation fails."""
    
    def __init__(self, message: str = "Validation failed", **kwargs):
        super().__init__(message, status_code=400, **kwargs)


class NotFoundError(DocuQueryException):
    """Raised when a requested resource is not found."""
    
    def __init__(self, message: str = "Resource not found", **kwargs):
        super().__init__(message, status_code=404, **kwargs)


class ConflictError(DocuQueryException):
    """Raised when a resource conflict occurs."""
    
    def __init__(self, message: str = "Resource conflict", **kwargs):
        super().__init__(message, status_code=409, **kwargs)


class RateLimitError(DocuQueryException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", **kwargs):
        super().__init__(message, status_code=429, **kwargs)


class TenantError(DocuQueryException):
    """Raised when tenant-related errors occur."""
    
    def __init__(self, message: str = "Tenant error", **kwargs):
        super().__init__(message, status_code=400, **kwargs)


class DocumentProcessingError(DocuQueryException):
    """Raised when document processing fails."""
    
    def __init__(self, message: str = "Document processing failed", **kwargs):
        super().__init__(message, status_code=500, **kwargs)


class VectorStoreError(DocuQueryException):
    """Raised when vector store operations fail."""
    
    def __init__(self, message: str = "Vector store operation failed", **kwargs):
        super().__init__(message, status_code=500, **kwargs)


class LLMError(DocuQueryException):
    """Raised when LLM operations fail."""
    
    def __init__(self, message: str = "LLM operation failed", **kwargs):
        super().__init__(message, status_code=500, **kwargs)
