FROM python:3.11-slim

# Install system dependencies for audio and ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    portaudio19-dev \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose port
EXPOSE 8003

# Run the FastAPI app
CMD ["python", "-m", "iss_module.service"]
