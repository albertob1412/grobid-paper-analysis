FROM python:3.11-slim

LABEL maintainer="albertob1412"
LABEL description="Open Science and AI - Text Analysis Pipeline"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY papers/ ./papers/

# Create outputs directory
RUN mkdir -p outputs

# Set environment variable for Grobid URL (can be overridden)
ENV GROBID_URL=http://host.docker.internal:8070/api/processFulltextDocument

# Default command
CMD ["python", "src/main.py"]
