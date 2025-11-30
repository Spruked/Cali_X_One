FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
ENV SEED_VAULT_PATH=/app/seed_vault
ENV RUNTIME_PATH=/app/runtime
ENV SERVICE_NAME=anterior-helix

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]