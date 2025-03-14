import os
import psycopg2
import numpy as np
from PIL import Image
import io
from typing import List, Dict, Union, Optional, Tuple
from pathlib import Path
import torch
from dotenv import load_dotenv
from app.model_loader import download_or_load_clip_model

class ImageSearch:
    """
    A class for searching similar images based on text queries or image inputs.
    Uses CLIP model for generating embeddings and pgvector for similarity search.
    """
    
    def __init__(self):
        """
        Initialize the ImageSearch class.
        
        Args:
            model_name: The name of the CLIP model to use for generating embeddings.
        """
        # Load environment variables
        load_dotenv()
        
        # Load CLIP model and processor using the shared loader
        self.model, self.processor = download_or_load_clip_model()
        
        # Database connection parameters
        self.db_params = {
            "host": os.getenv("DB_HOST"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "port": os.getenv("DB_PORT")
        }
    
    def get_db_connection(self):
        """Get a connection to the database."""
        return psycopg2.connect(**self.db_params)
    
    def get_image_embedding(self, image: Image.Image) -> np.ndarray:
        """
        Generate an embedding for an image.
        
        Args:
            image: A PIL Image object.
            
        Returns:
            A numpy array containing the image embedding.
        """
        inputs = self.processor(images=image, return_tensors="pt", padding=True)
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
        return image_features.detach().numpy().flatten()
    
    def get_text_embedding(self, text: str) -> np.ndarray:
        """
        Generate an embedding for a text query.
        
        Args:
            text: A text string.
            
        Returns:
            A numpy array containing the text embedding.
        """
        inputs = self.processor(text=text, return_tensors="pt", padding=True)
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
        return text_features.detach().numpy().flatten()
    
    def search_by_text(self, query: str, limit: int = 5) -> List[Dict[str, Union[str, float]]]:
        """
        Search for similar images using a text query.
        
        Args:
            query: A text string to search for.
            limit: Maximum number of results to return.
            
        Returns:
            A list of dictionaries containing the image path and similarity score.
        """
        embedding = self.get_text_embedding(query)
        return self._search_by_embedding(embedding, limit)
    
    def search_by_image(self, image: Image.Image, limit: int = 5) -> List[Dict[str, Union[str, float]]]:
        """
        Search for similar images using an image.
        
        Args:
            image: A PIL Image object.
            limit: Maximum number of results to return.
            
        Returns:
            A list of dictionaries containing the image path and similarity score.
        """
        embedding = self.get_image_embedding(image)
        return self._search_by_embedding(embedding, limit)
    
    def search_by_image_file(self, image_path: str, limit: int = 5) -> List[Dict[str, Union[str, float]]]:
        """
        Search for similar images using an image file.
        
        Args:
            image_path: Path to the image file.
            limit: Maximum number of results to return.
            
        Returns:
            A list of dictionaries containing the image path and similarity score.
        """
        image = Image.open(image_path)
        return self.search_by_image(image, limit)
    
    def search_by_image_bytes(self, image_bytes: bytes, limit: int = 5) -> List[Dict[str, Union[str, float]]]:
        """
        Search for similar images using image bytes.
        
        Args:
            image_bytes: Image data as bytes.
            limit: Maximum number of results to return.
            
        Returns:
            A list of dictionaries containing the image path and similarity score.
        """
        image = Image.open(io.BytesIO(image_bytes))
        return self.search_by_image(image, limit)
    
    def _search_by_embedding(self, embedding: np.ndarray, limit: int = 5) -> List[Dict[str, Union[str, float]]]:
        """
        Search for similar images using an embedding.
        
        Args:
            embedding: A numpy array containing the embedding.
            limit: Maximum number of results to return.
            
        Returns:
            A list of dictionaries containing the image path and similarity score.
        """
        conn = self.get_db_connection()
        cur = conn.cursor()
        
        # Search for similar images using cosine similarity
        cur.execute("""
            SELECT path, embedding <=> %s::vector AS distance
            FROM images
            ORDER BY distance
            LIMIT %s
        """, (embedding.tolist(), limit))
        
        results = cur.fetchall()
        cur.close()
        conn.close()
        
        return [{"path": path, "distance": float(distance)} for path, distance in results]
    
    def add_image(self, image: Image.Image, path: str) -> bool:
        """
        Add an image to the database.
        
        Args:
            image: A PIL Image object.
            path: Path to store for the image.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            embedding = self.get_image_embedding(image)
            
            conn = self.get_db_connection()
            cur = conn.cursor()
            
            # Store the image path and its embedding
            cur.execute(
                "INSERT INTO images (path, embedding) VALUES (%s, %s::vector) ON CONFLICT (path) DO UPDATE SET embedding = EXCLUDED.embedding",
                (path, embedding.tolist())
            )
            
            conn.commit()
            cur.close()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error adding image: {e}")
            return False
    
    def add_image_file(self, image_path: str, db_path: Optional[str] = None) -> bool:
        """
        Add an image file to the database.
        
        Args:
            image_path: Path to the image file.
            db_path: Path to store in the database. If None, uses image_path.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            image = Image.open(image_path)
            return self.add_image(image, db_path or image_path)
        except Exception as e:
            print(f"Error adding image file: {e}")
            return False
    
    def add_image_bytes(self, image_bytes: bytes, path: str) -> bool:
        """
        Add image bytes to the database.
        
        Args:
            image_bytes: Image data as bytes.
            path: Path to store for the image.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
            return self.add_image(image, path)
        except Exception as e:
            print(f"Error adding image bytes: {e}")
            return False
    
    def batch_add_images(self, image_paths: List[str], db_paths: Optional[List[str]] = None) -> Tuple[int, int]:
        """
        Add multiple images to the database.
        
        Args:
            image_paths: List of paths to image files.
            db_paths: List of paths to store in the database. If None, uses image_paths.
            
        Returns:
            A tuple of (number of successful additions, number of failed additions).
        """
        success_count = 0
        fail_count = 0
        
        for i, image_path in enumerate(image_paths):
            db_path = db_paths[i] if db_paths and i < len(db_paths) else image_path
            if self.add_image_file(image_path, db_path):
                success_count += 1
            else:
                fail_count += 1
        
        return success_count, fail_count 