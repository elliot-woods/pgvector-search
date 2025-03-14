# PGVector Image Search

Retrieve relevant images given a search query (i.e. "a green tree") from a postgres table

## Setup

1. Clone the repository
2. Create a `.env` file with the following variables:
   ```
   DB_HOST=db
   DB_PORT=5432
   DB_NAME=imagedb
   DB_USER=postgres
   DB_PASSWORD=postgres
   IMAGES_DIR=data/test_images
   MODELS_DIR=models
   EMBEDDINGS_DIR=embeddings
   MODEL_NAME=openai/clip-vit-base-patch32
   ```
3. Setup with:
   ```
   make start
   ```
4. Test with:
   ```
   make test-search-text
   ```

### API Endpoints

The FastAPI application exposes the following endpoints:

- `GET /search-by-text?query=<text>&limit=<int>`: Search for similar images using a text query
- `POST /upload`: Upload an image and store its embedding in the database
- `POST /search-by-image?limit=<int>`: Search for similar images using an uploaded image


## How It Works

1. Images are processed using the CLIP model to generate embeddings
2. Embeddings are stored in a PostgreSQL database with pgvector extension
3. When searching, the query (text or image) is converted to an embedding
4. The database performs a similarity search using cosine similarity
5. The most similar images are returned, along with their similarity scores
