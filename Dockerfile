FROM python:3.11-slim

# Install system dependencies for audio, ffmpeg, and SKG requirements
RUN apt-get update && apt-get install -y \
    ffmpeg \
    portaudio19-dev \
    gcc \
    g++ \
    make \
    sqlite3 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install SKG core module
COPY skg-core/ ./skg-core/
RUN cd skg-core && pip install -e .

# Copy the entire project
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/seed_vault

# Set environment variables for SKG
ENV PYTHONPATH=/app:/app/skg-core:$PYTHONPATH
ENV SKG_DB_PATH=/app/data/skg.db

# Expose ports (8003 for main service, 8004 for SKG service)
EXPOSE 8003 8004

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8003/health || exit 1

# Run the enhanced Cali X One system with SKG
CMD ["python", "run_server.py"]
