# DocuQuery AI - API Contracts

## Overview

This document defines the API contracts for DocuQuery AI, including request/response schemas, authentication requirements, and example payloads. All endpoints are prefixed with `/api/v1/` and require proper authentication unless otherwise specified.

## Authentication

### Headers Required
```
Authorization: Bearer <jwt_token>
X-Tenant-ID: <tenant_identifier>
Content-Type: application/json
```

## Authentication Endpoints

### POST /auth/login

**Description**: Authenticate user with email/password and return JWT tokens

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "secure_password_123"
}
```

**Response (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "tenant_id": "tenant_456"
  }
}
```

**Response (401)**:
```json
{
  "error": "Invalid credentials",
  "code": "AUTH_001",
  "details": "Email or password is incorrect"
}
```

### POST /auth/refresh

**Description**: Refresh access token using refresh token

**Request Body**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### POST /auth/logout

**Description**: Invalidate refresh token and logout user

**Request Body**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200)**:
```json
{
  "message": "Successfully logged out"
}
```

## Document Management Endpoints

### POST /documents/upload-url

**Description**: Get presigned URL for direct file upload to storage

**Request Body**:
```json
{
  "filename": "document.pdf",
  "content_type": "application/pdf",
  "file_size": 2048576,
  "metadata": {
    "title": "Sample Document",
    "description": "A sample PDF document for testing",
    "tags": ["sample", "pdf", "test"]
  }
}
```

**Response (200)**:
```json
{
  "upload_url": "https://storage.example.com/upload?token=abc123...",
  "document_id": "doc_789",
  "expires_at": "2024-01-15T10:30:00Z",
  "fields": {
    "key": "tenants/tenant_456/documents/doc_789/document.pdf"
  }
}
```

### GET /documents

**Description**: List documents with pagination and filtering

**Query Parameters**:
- `page`: Page number (default: 1)
- `size`: Page size (default: 20, max: 100)
- `search`: Search query for title/description
- `status`: Document status filter
- `type`: Document type filter
- `tags`: Comma-separated tag list

**Response (200)**:
```json
{
  "documents": [
    {
      "id": "doc_789",
      "title": "Sample Document",
      "filename": "document.pdf",
      "content_type": "application/pdf",
      "file_size": 2048576,
      "status": "processed",
      "created_at": "2024-01-15T09:00:00Z",
      "updated_at": "2024-01-15T09:15:00Z",
      "metadata": {
        "title": "Sample Document",
        "description": "A sample PDF document for testing",
        "tags": ["sample", "pdf", "test"]
      }
    }
  ],
  "pagination": {
    "page": 1,
    "size": 20,
    "total": 1,
    "pages": 1
  }
}
```

### GET /documents/{document_id}

**Description**: Get document details and processing status

**Response (200)**:
```json
{
  "id": "doc_789",
  "title": "Sample Document",
  "filename": "document.pdf",
  "content_type": "application/pdf",
  "file_size": 2048576,
  "status": "processed",
  "processing_progress": 100,
  "created_at": "2024-01-15T09:00:00Z",
  "updated_at": "2024-01-15T09:15:00Z",
  "metadata": {
    "title": "Sample Document",
    "description": "A sample PDF document for testing",
    "tags": ["sample", "pdf", "test"]
  },
  "chunks": [
    {
      "id": "chunk_001",
      "content": "This is the first chunk of the document...",
      "page_number": 1,
      "chunk_index": 0,
      "embedding_status": "completed"
    }
  ]
}
```

## Query Endpoints

### POST /query

**Description**: Submit a natural language query and get AI-generated answer with citations

**Request Body**:
```json
{
  "query": "What are the main requirements for the project?",
  "filters": {
    "document_ids": ["doc_789", "doc_790"],
    "date_range": {
      "start": "2024-01-01",
      "end": "2024-01-31"
    },
    "tags": ["requirements", "specifications"]
  },
  "options": {
    "include_citations": true,
    "max_citations": 5,
    "response_format": "detailed"
  }
}
```

**Response (200)**:
```json
{
  "query_id": "query_123",
  "query": "What are the main requirements for the project?",
  "answer": "Based on the analyzed documents, the main requirements for the project include:\n\n1. **User Authentication**: Implement secure JWT-based authentication with OAuth2 support\n2. **Multi-tenancy**: Support multiple tenant organizations with data isolation\n3. **Document Processing**: Handle PDF, Word, and text documents with OCR capabilities\n4. **Vector Search**: Implement semantic search using embeddings and vector databases\n5. **AI Integration**: Provide intelligent Q&A using large language models\n\nThese requirements ensure the system can scale to enterprise needs while maintaining security and performance standards.",
  "citations": [
    {
      "document_id": "doc_789",
      "document_title": "Project Requirements Specification",
      "chunk_id": "chunk_001",
      "content": "The system must implement secure user authentication...",
      "page_number": 1,
      "relevance_score": 0.95
    },
    {
      "document_id": "doc_790",
      "document_title": "Technical Architecture Document",
      "chunk_id": "chunk_005",
      "content": "Multi-tenancy is a core requirement...",
      "page_number": 3,
      "relevance_score": 0.92
    }
  ],
  "metadata": {
    "processing_time_ms": 1250,
    "chunks_retrieved": 15,
    "chunks_reranked": 8,
    "llm_provider": "openai",
    "model_used": "gpt-4"
  },
  "created_at": "2024-01-15T10:00:00Z"
}
```

### GET /query/{query_id}

**Description**: Get query details and processing status

**Response (200)**:
```json
{
  "id": "query_123",
  "query": "What are the main requirements for the project?",
  "status": "completed",
  "answer": "Based on the analyzed documents...",
  "citations": [...],
  "metadata": {...},
  "created_at": "2024-01-15T10:00:00Z",
  "completed_at": "2024-01-15T10:00:01Z"
}
```

### GET /query/history

**Description**: Get user's query history with pagination

**Query Parameters**:
- `page`: Page number (default: 1)
- `size`: Page size (default: 20, max: 100)
- `date_range`: Date range filter

**Response (200)**:
```json
{
  "queries": [
    {
      "id": "query_123",
      "query": "What are the main requirements for the project?",
      "status": "completed",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "size": 20,
    "total": 1,
    "pages": 1
  }
}
```

## User Management Endpoints

### GET /users/me

**Description**: Get current user profile information

**Response (200)**:
```json
{
  "id": "user_123",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user",
  "tenant_id": "tenant_456",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T09:00:00Z",
  "preferences": {
    "language": "en",
    "timezone": "UTC",
    "notifications": {
      "email": true,
      "push": false
    }
  }
}
```

### PUT /users/me

**Description**: Update current user profile

**Request Body**:
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "preferences": {
    "language": "en",
    "timezone": "America/New_York",
    "notifications": {
      "email": true,
      "push": true
    }
  }
}
```

**Response (200)**:
```json
{
  "id": "user_123",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Smith",
  "role": "user",
  "tenant_id": "tenant_456",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z",
  "preferences": {
    "language": "en",
    "timezone": "America/New_York",
    "notifications": {
      "email": true,
      "push": true
    }
  }
}
```

## Health & Information Endpoints

### GET /health

**Description**: Check system health and dependencies

**Response (200)**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00Z",
  "version": "0.1.0",
  "dependencies": {
    "database": "healthy",
    "redis": "healthy",
    "qdrant": "healthy",
    "openai": "healthy"
  },
  "uptime": "2d 5h 30m 15s"
}
```

### GET /info

**Description**: Get system information and capabilities

**Response (200)**:
```json
{
  "name": "DocuQuery AI",
  "version": "0.1.0",
  "description": "Production-ready AI Document Q&A API",
  "features": {
    "multi_tenancy": true,
    "oauth2": true,
    "vector_search": true,
    "document_ocr": true,
    "streaming": true
  },
  "supported_formats": [
    "pdf",
    "docx",
    "txt",
    "md"
  ],
  "llm_providers": [
    "openai",
    "anthropic",
    "azure_openai"
  ]
}
```

## Error Responses

### Standard Error Format
```json
{
  "error": "Error message description",
  "code": "ERROR_CODE",
  "details": "Additional error details",
  "timestamp": "2024-01-15T10:00:00Z",
  "request_id": "req_456"
}
```

### Common Error Codes
- `AUTH_001`: Invalid credentials
- `AUTH_002`: Token expired
- `AUTH_003`: Insufficient permissions
- `TENANT_001`: Invalid tenant ID
- `DOC_001`: Document not found
- `DOC_002`: Document processing failed
- `QUERY_001`: Query processing failed
- `VALIDATION_001`: Invalid request data
- `RATE_LIMIT_001`: Rate limit exceeded
- `INTERNAL_001`: Internal server error

## Rate Limiting

### Limits
- **Authentication endpoints**: 5 requests per minute per IP
- **Document endpoints**: 20 requests per minute per user
- **Query endpoints**: 30 requests per minute per user
- **User endpoints**: 10 requests per minute per user

### Headers
```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 25
X-RateLimit-Reset: 1642233600
```

## Pagination

### Standard Pagination Format
```json
{
  "pagination": {
    "page": 1,
    "size": 20,
    "total": 100,
    "pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

### Query Parameters
- `page`: Page number (1-based, default: 1)
- `size`: Page size (default: 20, max: 100)
- `sort`: Sort field (default: created_at)
- `order`: Sort order (asc/desc, default: desc)
