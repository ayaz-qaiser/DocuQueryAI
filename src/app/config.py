"""
DocuQuery AI - Configuration Management

This module contains the application configuration using Pydantic Settings.
All configuration values are loaded from environment variables with sensible defaults.
"""

from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Application Configuration
    APP_NAME: str = Field(default="DocuQuery AI", description="Application name")
    APP_VERSION: str = Field(default="0.1.0", description="Application version")
    DEBUG: bool = Field(default=False, description="Debug mode")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    ENVIRONMENT: str = Field(default="development", description="Environment name")
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    WORKERS: int = Field(default=4, description="Number of worker processes")
    RELOAD: bool = Field(default=False, description="Auto-reload on code changes")
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/docuquery_ai",
        description="Database connection URL"
    )
    DATABASE_POOL_SIZE: int = Field(default=20, description="Database connection pool size")
    DATABASE_MAX_OVERFLOW: int = Field(default=30, description="Database max overflow")
    DATABASE_POOL_TIMEOUT: int = Field(default=30, description="Database pool timeout")
    
    # Redis Configuration
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )
    REDIS_POOL_SIZE: int = Field(default=10, description="Redis connection pool size")
    REDIS_MAX_CONNECTIONS: int = Field(default=20, description="Redis max connections")
    
    # Qdrant Configuration
    QDRANT_URL: str = Field(
        default="http://localhost:6333",
        description="Qdrant vector database URL"
    )
    QDRANT_API_KEY: Optional[str] = Field(default=None, description="Qdrant API key")
    QDRANT_TIMEOUT: int = Field(default=30, description="Qdrant request timeout")
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API key")
    OPENAI_ORGANIZATION: Optional[str] = Field(default=None, description="OpenAI organization")
    OPENAI_MODEL: str = Field(default="gpt-4", description="OpenAI model name")
    OPENAI_EMBEDDING_MODEL: str = Field(default="text-embedding-ada-002", description="OpenAI embedding model")
    OPENAI_MAX_TOKENS: int = Field(default=4000, description="OpenAI max tokens")
    OPENAI_TEMPERATURE: float = Field(default=0.1, description="OpenAI temperature")
    
    # Authentication Configuration
    JWT_SECRET: str = Field(
        default="your_jwt_secret_key_here_make_it_long_and_random",
        description="JWT secret key"
    )
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="JWT access token expiry")
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, description="JWT refresh token expiry")
    
    # OAuth2 Configuration
    GOOGLE_CLIENT_ID: Optional[str] = Field(default=None, description="Google OAuth2 client ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(default=None, description="Google OAuth2 client secret")
    MICROSOFT_CLIENT_ID: Optional[str] = Field(default=None, description="Microsoft OAuth2 client ID")
    MICROSOFT_CLIENT_SECRET: Optional[str] = Field(default=None, description="Microsoft OAuth2 client secret")
    
    # File Storage Configuration
    STORAGE_TYPE: str = Field(default="local", description="Storage type (local, s3, azure, gcp)")
    STORAGE_BUCKET: str = Field(default="docuquery-ai-documents", description="Storage bucket name")
    STORAGE_REGION: str = Field(default="us-east-1", description="Storage region")
    STORAGE_ACCESS_KEY: Optional[str] = Field(default=None, description="Storage access key")
    STORAGE_SECRET_KEY: Optional[str] = Field(default=None, description="Storage secret key")
    
    # Rate Limiting Configuration
    RATE_LIMIT_REQUESTS: int = Field(default=100, description="Rate limit requests per window")
    RATE_LIMIT_WINDOW: int = Field(default=60, description="Rate limit window in seconds")
    
    # Feature Flags
    FEATURE_MULTI_TENANCY: bool = Field(default=True, description="Enable multi-tenancy")
    FEATURE_OAUTH_ENABLED: bool = Field(default=True, description="Enable OAuth2 authentication")
    FEATURE_DOCUMENT_OCR: bool = Field(default=True, description="Enable document OCR")
    FEATURE_VECTOR_SEARCH: bool = Field(default=True, description="Enable vector search")
    FEATURE_CITATION_GENERATION: bool = Field(default=True, description="Enable citation generation")
    
    # Monitoring Configuration
    SENTRY_DSN: Optional[str] = Field(default=None, description="Sentry DSN for error tracking")
    PROMETHEUS_ENABLED: bool = Field(default=True, description="Enable Prometheus metrics")
    PROMETHEUS_PORT: int = Field(default=9090, description="Prometheus metrics port")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    
    if _settings is None:
        _settings = Settings()
    
    return _settings


def reload_settings() -> Settings:
    """Reload settings from environment variables."""
    global _settings
    _settings = Settings()
    return _settings
