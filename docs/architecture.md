# DocuQuery AI - Architecture Overview

## System Architecture

DocuQuery AI follows a clean, modular architecture designed for enterprise-scale document intelligence and retrieval-augmented generation (RAG). The system is built with clear domain boundaries, separation of concerns, and extensibility in mind.

## Core Modules

### Authentication & Authorization (`src/app/auth/`)
- **JWT-based authentication** with configurable token expiration
- **OAuth2 integration** supporting Google and Microsoft identity providers
- **Role-based access control (RBAC)** with fine-grained permissions
- **Multi-tenant isolation** through tenant-scoped policies
- **Session management** with Redis-backed storage

### Multi-Tenancy (`src/app/tenants/`)
- **Header-based tenant identification** using `X-Tenant-ID`
- **Tenant isolation** at database and application levels
- **Tenant-specific configurations** for features and limits
- **Cross-tenant data segregation** enforced through middleware

### User Management (`src/app/users/`)
- **User lifecycle management** (create, update, deactivate)
- **Profile management** with customizable attributes
- **Role assignment** and permission inheritance
- **Audit logging** for compliance requirements

### Document Management (`src/app/documents/`)
- **Document ingestion pipeline** supporting multiple formats
- **Metadata extraction** and enrichment
- **Version control** and change tracking
- **Storage abstraction** supporting local, S3, Azure, and GCP

### Retrieval Engine (`src/app/retrieval/`)
- **Vector search** using Qdrant for semantic similarity
- **Hybrid search** combining vector and keyword approaches
- **Reranking** using cross-encoders for relevance
- **Citation generation** with source attribution

### LLM Integration (`src/app/llm/`)
- **Provider abstraction** supporting OpenAI, Anthropic, and Azure
- **Prompt management** using Jinja2 templates
- **Response streaming** for real-time interactions
- **Fallback strategies** for provider failures

### Background Processing (`src/app/background/`)
- **Celery-based task queue** with Redis backend
- **Document processing** pipeline orchestration
- **Embedding generation** and vector indexing
- **Async notification** system for long-running operations

## Request Lifecycle

### 1. Authentication & Authorization
- **Request validation** and tenant identification
- **JWT token verification** and user authentication
- **Permission checking** against RBAC policies
- **Tenant context** establishment for request processing

### 2. Middleware Processing
- **Request ID generation** for tracing
- **Logging and monitoring** with structured logs
- **Rate limiting** per tenant and user
- **Security headers** and CORS handling
- **Request timing** and performance metrics

### 3. Routing & Dispatching
- **API versioning** with `/api/v1/` prefix
- **Feature routing** based on tenant capabilities
- **Request validation** using Pydantic schemas
- **Dependency injection** for shared resources

### 4. Service Layer
- **Business logic** implementation
- **Data validation** and transformation
- **External service** integration
- **Error handling** and recovery

### 5. Repository Layer
- **Data persistence** and retrieval
- **Query optimization** and caching
- **Transaction management** and rollback
- **Multi-tenant** data isolation

### 6. Background Tasks
- **Async processing** for long-running operations
- **Event publishing** for system integration
- **Status tracking** and progress updates
- **Failure handling** and retry logic

## Multi-Tenancy Strategy

### Tenant Identification
- **Header-based routing** using `X-Tenant-ID`
- **Tenant validation** against active tenant registry
- **Fallback handling** for missing tenant headers
- **Tenant context** propagation through request lifecycle

### Data Isolation
- **Database-level isolation** using tenant-specific schemas
- **Application-level filtering** for cross-tenant queries
- **Cache isolation** with tenant-prefixed keys
- **File storage** separation by tenant

### Feature Management
- **Tenant-specific feature flags** for gradual rollouts
- **Usage limits** and quota management
- **Custom configurations** for tenant preferences
- **A/B testing** support per tenant

## RAG (Retrieval-Augmented Generation) Flow

### 1. Document Ingestion
- **File upload** and validation
- **Format detection** and parser selection
- **Content extraction** and cleaning
- **Chunking strategy** for optimal retrieval
- **Metadata enrichment** and tagging

### 2. Embedding Generation
- **Text preprocessing** and normalization
- **Vector embedding** using OpenAI or alternatives
- **Chunk-level embeddings** for granular search
- **Batch processing** for efficiency
- **Quality validation** and error handling

### 3. Vector Indexing
- **Qdrant collection** management
- **Index optimization** for search performance
- **Metadata filtering** capabilities
- **Real-time updates** for fresh content
- **Backup and recovery** procedures

### 4. Query Processing
- **Query understanding** and intent classification
- **Vector search** for semantic similarity
- **Hybrid search** combining multiple approaches
- **Result ranking** and relevance scoring
- **Context window** optimization

### 5. Reranking & Selection
- **Cross-encoder models** for relevance scoring
- **Diversity optimization** for comprehensive coverage
- **Source balancing** across document types
- **Confidence scoring** for answer quality
- **Fallback strategies** for edge cases

### 6. Answer Generation
- **Prompt engineering** with Jinja2 templates
- **Context assembly** from retrieved chunks
- **LLM integration** with streaming responses
- **Citation generation** with source links
- **Answer validation** and quality checks

## Data Flow Architecture

### Synchronous Operations
- **User authentication** and session management
- **Document metadata** queries and updates
- **Search requests** with immediate responses
- **User profile** management and settings

### Asynchronous Operations
- **Document processing** and embedding generation
- **Vector indexing** and collection updates
- **Background maintenance** and optimization
- **Notification delivery** and event processing

### Event-Driven Communication
- **Document processing** completion events
- **User activity** tracking and analytics
- **System health** monitoring and alerting
- **Integration webhooks** for external systems

## Scalability Considerations

### Horizontal Scaling
- **Stateless API services** for load balancing
- **Worker pool** scaling for background tasks
- **Database read replicas** for query distribution
- **Cache clustering** for Redis scalability

### Performance Optimization
- **Connection pooling** for database efficiency
- **Response caching** for repeated queries
- **Batch processing** for bulk operations
- **Async I/O** for non-blocking operations

### Monitoring & Observability
- **Structured logging** with correlation IDs
- **Metrics collection** for performance tracking
- **Health checks** for service dependencies
- **Distributed tracing** for request flows

## Security Architecture

### Authentication & Authorization
- **JWT token security** with proper expiration
- **OAuth2 integration** with secure redirects
- **Role-based permissions** with principle of least privilege
- **Multi-factor authentication** support

### Data Protection
- **Encryption at rest** for sensitive data
- **TLS encryption** for data in transit
- **Tenant isolation** preventing data leakage
- **Audit logging** for compliance requirements

### API Security
- **Rate limiting** to prevent abuse
- **Input validation** and sanitization
- **CORS configuration** for web security
- **Security headers** for browser protection
