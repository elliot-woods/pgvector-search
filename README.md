# pg_vector Image Search

Retrieve relevant images given a search query (i.e. "a green tree") from a postgres table

## Setup with **test images** (located in data/test_images)

1. Clone the repository
2. Create a `.env` file (you can copy contents of the `.env.example` for testing)
3. Create the DB and start API with:
   ```
   TESTING=1 make start
   ```
4. Test the API with:
   ```
   make test-api SEARCH="your search query" LIMIT=5
   ```
   - Example: make test-api SEARCH="a green tree" LIMIT=2
   - Example: make test-api SEARCH="sports car" LIMIT=2


## Setup with **R2 images** (will be located in data/images)
**IMPORTANT** In order to download images from an R2 bucket you need to have the following env vars in your `.env` file:
   ```
   R2_ENDPOINT_URL=???
   R2_ACCESS_KEY_ID=???
   R2_SECRET_ACCESS_KEY=???
   R2_BUCKET_NAME=???
   MAX_IMAGES=100
   ```

1. Clone the repository
2. Create a `.env` file (you can copy contents of the `.env.example` for testing)
3. Download R2 images with (you can modify how many images to download with the `MAX_IMAGES` env var located in your `.env` file):
   ```
   make download-images
   ```
3. Create the DB and start API with:
   ```
   make start
   ```
4. Test the API with:
   ```
   make test-api SEARCH="your search query" LIMIT=5
   ```
   - Example: make test-api SEARCH="a green tree" LIMIT=2
   - Example: make test-api SEARCH="sports car" LIMIT=2


### API Endpoints

The FastAPI application exposes the following endpoints:

- `GET /search-by-text?query=<text>&limit=<int>`: Search for similar images using a text query
- [WIP] `POST /upload`: Upload an image and store its embedding in the database
- [WIP] `POST /search-by-image?limit=<int>`: Search for similar images using an uploaded image


## How It Works

1. Images are processed using the CLIP model to generate embeddings
2. Embeddings are stored in a PostgreSQL database with pgvector extension
3. When searching, the query (text or image) is converted to an embedding
4. The database performs a similarity search using cosine similarity
5. The most similar images are returned, along with their similarity scores
