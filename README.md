# PGVector Image Search

This project demonstrates how to use pgvector for image similarity search using CLIP embeddings.

## Overview

The project consists of:

1. A PostgreSQL database with pgvector extension for vector similarity search
2. A Python class for generating embeddings and searching for similar images
3. A FastAPI application for exposing the search functionality via an API

## Setup

1. Clone the repository
2. Create a `.env` file with the following variables:
   ```
   DB_HOST=db
   DB_PORT=5432
   DB_NAME=imagedb
   DB_USER=postgres
   DB_PASSWORD=postgres
   IMAGES_DIR=data/images
   ```
3. Run the setup script:
   ```
   # Option 1: Using make
   make setup
   
   # Option 2: Running the script directly
   chmod +x scripts/setup.sh scripts/setup_db.sh scripts/setup_embeddings.sh
   ./scripts/setup.sh
   ```
4. Start the application:
   ```
   docker-compose up -d
   ```

## Using the ImageSearch Class

The `ImageSearch` class provides a simple interface for searching for similar images based on text queries or image inputs.

### Basic Usage

```python
from image_search import ImageSearch
from PIL import Image

# Initialize the ImageSearch class
image_search = ImageSearch()

# Search by text query
results = image_search.search_by_text("a cat sitting on a couch", limit=5)

# Search by image file
results = image_search.search_by_image_file("path/to/image.jpg", limit=5)

# Search by PIL Image
image = Image.open("path/to/image.jpg")
results = image_search.search_by_image(image, limit=5)

# Add an image to the database
success = image_search.add_image_file("path/to/image.jpg")

# Batch add images
image_paths = ["path/to/image1.jpg", "path/to/image2.jpg"]
success_count, fail_count = image_search.batch_add_images(image_paths)
```

### API Endpoints

The FastAPI application exposes the following endpoints:

- `GET /search?query=<text>&limit=<int>`: Search for similar images using a text query
- `POST /upload`: Upload an image and store its embedding in the database
- `POST /search-by-image?limit=<int>`: Search for similar images using an uploaded image

## Example

See `app/example.py` for a complete example of how to use the `ImageSearch` class.

```bash
python app/example.py
```

## How It Works

1. Images are processed using the CLIP model to generate embeddings
2. Embeddings are stored in a PostgreSQL database with pgvector extension
3. When searching, the query (text or image) is converted to an embedding
4. The database performs a similarity search using cosine similarity
5. The most similar images are returned, along with their similarity scores

## Dependencies

- Python 3.8+
- PostgreSQL with pgvector extension
- PyTorch
- Transformers (Hugging Face)
- FastAPI
- Pillow
- psycopg2-binary
- python-dotenv
- numpy 