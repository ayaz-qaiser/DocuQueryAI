#!/bin/bash

# DocuQuery AI - Development Environment Startup Script
# This script starts the local development environment using Docker Compose

set -e

echo "🚀 Starting DocuQuery AI development environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install it and try again."
    exit 1
fi

# Navigate to the project root (assuming script is run from scripts/ directory)
cd "$(dirname "$0")/.."

echo "📁 Project directory: $(pwd)"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env file created from .env.example"
        echo "⚠️  Please update .env with your actual configuration values"
    else
        echo "❌ .env.example not found. Please create a .env file manually."
        exit 1
    fi
fi

echo "🐳 Starting services with Docker Compose..."
docker-compose -f infra/compose.yml up -d

echo "⏳ Waiting for services to be ready..."
sleep 10

echo "🔍 Checking service health..."

# Check PostgreSQL
if docker-compose -f infra/compose.yml exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
    echo "✅ PostgreSQL is ready"
else
    echo "❌ PostgreSQL is not ready"
fi

# Check Redis
if docker-compose -f infra/compose.yml exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is ready"
else
    echo "❌ Redis is not ready"
fi

# Check Qdrant
if curl -f http://localhost:6333/health > /dev/null 2>&1; then
    echo "✅ Qdrant is ready"
else
    echo "❌ Qdrant is not ready"
fi

echo ""
echo "🎉 Development environment is starting up!"
echo ""
echo "📊 Service URLs:"
echo "   API: http://localhost:8000"
echo "   pgAdmin: http://localhost:5050"
echo "   Redis Commander: http://localhost:8081"
echo "   Qdrant: http://localhost:6333"
echo ""
echo "📚 Useful commands:"
echo "   View logs: docker-compose -f infra/compose.yml logs -f"
echo "   Stop services: docker-compose -f infra/compose.yml down"
echo "   Restart services: docker-compose -f infra/compose.yml restart"
echo ""
echo "⚠️  Note: This is a scaffolding project. Business logic is not implemented yet."
