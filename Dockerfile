FROM python:3.11-slim

WORKDIR /app

# Install system deps (needed by scikit-learn/numpy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only what the backend needs
COPY src/ ./src/
COPY data/vectors/ ./data/vectors/
COPY data/processed/ ./data/processed/
COPY backend/ ./backend/
COPY configs/ ./configs/

# Environment
ENV PYTHONPATH=.
ENV PYTHONUNBUFFERED=1

# Render injects $PORT at runtime
CMD uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
