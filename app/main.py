from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.image_search import ImageSearch

load_dotenv()

app = FastAPI(title="Image Similarity Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ImageSearch
image_search = ImageSearch()

@app.get("/search-by-text")
async def search_similar_images(query: str, limit: int = 5):
    """
    Search for similar images using a text query.
    
    Args:
        query: A text string to search for.
        limit: Maximum number of results to return.
        
    Returns:
        A list of dictionaries containing the image path and similarity score.
    """
    return image_search.search_by_text(query, limit)

@app.post("/upload")
async def upload_image(file: UploadFile):
    """
    Upload an image and store its embedding in the database.
    
    Args:
        file: The image file to upload.
        
    Returns:
        A dictionary containing a message and the filename.
    """
    # Read and process the image
    contents = await file.read()
    success = image_search.add_image_bytes(contents, file.filename)
    
    if success:
        return {"message": "Image uploaded successfully", "filename": file.filename}
    else:
        return {"message": "Failed to upload image", "filename": file.filename}

@app.post("/search-by-image")
async def search_by_image(file: UploadFile, limit: int = 5):
    """
    Search for similar images using an uploaded image.
    
    Args:
        file: The image file to search with.
        limit: Maximum number of results to return.
        
    Returns:
        A list of dictionaries containing the image path and similarity score.
    """
    # Read and process the image
    contents = await file.read()
    results = image_search.search_by_image_bytes(contents, limit)
    
    return results 