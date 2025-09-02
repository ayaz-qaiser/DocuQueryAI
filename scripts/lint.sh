#!/bin/bash

# DocuQuery AI - Linting and Type Checking Script
# This script runs code quality checks using Ruff and MyPy

set -e

echo "🔍 Running code quality checks for DocuQuery AI..."

# Navigate to the project root (assuming script is run from scripts/ directory)
cd "$(dirname "$0")/.."

echo "📁 Project directory: $(pwd)"

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed. Please install it first:"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d ".venv" ] && [ ! -f "poetry.lock" ]; then
    echo "⚠️  Dependencies not installed. Installing now..."
    poetry install --only dev
fi

echo "🧹 Running Ruff (linter and formatter)..."
poetry run ruff check src/
poetry run ruff format --check src/

echo "✅ Ruff checks completed"

echo "🔍 Running MyPy (type checker)..."
poetry run mypy src/

echo "✅ MyPy checks completed"

echo "🎉 All code quality checks passed!"
echo ""
echo "💡 Tips:"
echo "   - Run 'poetry run ruff format src/' to auto-format code"
echo "   - Run 'poetry run ruff check --fix src/' to auto-fix issues"
echo "   - Check pyproject.toml for configuration options"
