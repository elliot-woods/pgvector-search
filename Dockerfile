FROM python:3.9-slim

WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    nano \
    less \
    jq \
    htop \
    awscli \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files to the app directory
COPY . .

# Make all scripts executable
RUN chmod +x /app/scripts/setup.sh /app/scripts/setup_db.sh /app/scripts/setup_embeddings.sh /app/scripts/setup_embedding_index.sh /app/scripts/download_images.sh

# Start FastAPI app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"] 