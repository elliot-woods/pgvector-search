# pg_vector Image Search

Retrieve relevant images given a search query (i.e. "a green tree") from a postgres table

## Setup with **test images**
- Test images are already installed and located in `TEST_IMAGES_DIR`

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
   - Example: 
      `make test-api SEARCH="a green tree" LIMIT=4`
            
      Result:
      ```
      Testing /search-by-text with 'a green tree' query and limit 4...
      [
         {
            "path": "data/test_images/download-8.jpg",
            "distance": 0.7141705992776717
         },
         {
            "path": "data/test_images/download-11.jpg",
            "distance": 0.7194434540630541
         },
         {
            "path": "data/test_images/download-10.jpg",
            "distance": 0.7258576176052569
         },
         {
            "path": "data/test_images/download-9.jpg",
            "distance": 0.733280044322933
         }
      ]
      ```
   - Example: 
      `make test-api SEARCH="sports car" LIMIT=2`
            
      Result:
      ```
      Testing /search-by-text with 'sports car' query and limit 2...
      [
         {
            "path": "data/test_images/download-12.jpg",
            "distance": 0.7219719462600145
         },
         {
            "path": "data/test_images/download-14.jpg",
            "distance": 0.7226935017421838
         }
      ]
      ```



## Setup with **R2 images**
- Images will be installed to disk inside `IMAGES_DIR`

- **IMPORTANT** In order to download images from an R2 bucket you need to have the following env vars in your `.env` file:
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
   - Example: 
      `make test-api LIMIT=5 SEARCH="a person with pink hair"`
      
      Result:
      ```
      Testing /search-by-text with 'a person with pink hair' query and limit 5...
      [
         {
            "path": "data/images/rCN3WEHZ8Obdt.jpeg",
            "distance": 0.7135157371878005
         },
         {
            "path": "data/images/0S6IjibNm3pFg.png",
            "distance": 0.7614015521782136
         },
         {
            "path": "data/images/7w0IxLMNKpAZX.png",
            "distance": 0.7614776395247627
         },
         {
            "path": "data/images/228CtojAiLoNI.jpeg",
            "distance": 0.7670808304838583
         },
         {
            "path": "data/images/0_-NKJjR6QfSE.png",
            "distance": 0.768500314713227
         }
      ]
      ```


## API Endpoints

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
