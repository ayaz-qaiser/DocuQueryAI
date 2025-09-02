# DocuQuery AI

A production-ready AI Document Q&A API built with FastAPI, designed for enterprise document intelligence and retrieval-augmented generation (RAG).

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd docuquery-ai

# Install dependencies
poetry install

# Start local development environment
./scripts/dev_up.sh

# Run linting
./scripts/lint.sh
```

## 🏗️ Tech Stack

- **API Framework**: FastAPI with async/await support
- **Database**: PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **Vector Database**: Qdrant for semantic search and similarity
- **Cache**: Redis for session management and job queues
- **AI/ML**: OpenAI GPT-4 + embeddings, with support for multiple providers
- **Authentication**: JWT + OAuth2 (Google, Microsoft) with RBAC
- **Background Processing**: Celery with Redis backend
- **Testing**: Pytest with unit, integration, and E2E test suites
- **Code Quality**: Ruff (linting), MyPy (type checking)
- **Containerization**: Docker + Docker Compose for local development
- **Package Management**: Poetry for dependency management

## 📁 Architecture Overview

The application follows a clean, modular architecture with clear domain boundaries:

- **Multi-tenant design** with header-based tenant identification
- **Domain-driven structure** separating concerns (auth, documents, retrieval, LLM)
- **Background task processing** for document ingestion and embedding generation
- **Pluggable AI providers** supporting multiple LLM and embedding services
- **Event-driven messaging** for asynchronous operations
- **Comprehensive middleware** for logging, rate limiting, and security

## ⚠️ Important Note

**This repository contains only the architectural scaffolding and placeholder content.** Business logic, actual implementations, and production configurations are intentionally omitted at this stage.

The codebase serves as a blueprint for:
- Understanding the overall system architecture
- Planning development phases
- Setting up development environments
- Establishing coding patterns and conventions

## 🔧 Development Status

- ✅ Project structure and architecture defined
- ✅ Configuration and dependency management setup
- ✅ Docker development environment configured
- ✅ CI/CD pipeline skeleton created
- ✅ Documentation and API contracts outlined
- 🚧 Business logic implementation (not included)
- 🚧 Production deployment configurations (not included)
- 🚧 Security hardening and compliance (not included)

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [API Contracts](docs/api-contracts.md)
- [Tenancy and RBAC](docs/tenancy-and-rbac.md)
- [Data Ingestion Pipeline](docs/data-ingestion-pipeline.md)
- [Operations Runbooks](docs/ops-runbooks.md)

## 🤝 Contributing

1. Review the architecture documentation
2. Set up the development environment
3. Create feature branches from `main`
4. Follow the established patterns and structure
5. Ensure all tests pass and linting requirements are met

## 📄 License

[License information to be added]
