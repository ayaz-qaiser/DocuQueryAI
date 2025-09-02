FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app/src

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy poetry configuration
COPY pyproject.toml poetry.lock* ./

# TODO: Add poetry install steps later
# RUN pip install poetry
# RUN poetry config virtualenvs.create false
# RUN poetry install --no-dev --no-interaction --no-ansi

# Copy source code
COPY src/ ./src/

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 8000

# TODO: Add proper startup command later
CMD ["echo", "TODO: Add uvicorn startup command"]
