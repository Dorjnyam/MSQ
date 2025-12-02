FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# Install system dependencies that some packages may need
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       git \
       ffmpeg \
       libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (for better caching)
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for uploads and chroma_db
RUN mkdir -p uploads chroma_db

# Fly.io uses port 8080 by default
EXPOSE 8080

# Use environment variable for port
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}
