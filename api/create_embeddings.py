import os
import csv
from PIL import Image
from dotenv import load_dotenv
from pathlib import Path
import numpy as np
from load_embedding_model import download_or_load_clip_model

load_dotenv()

def create_embeddings():
    # Initialize CLIP model and processor
    print("Initializing CLIP model and processor...")
 
    # Load model and processor using the shared loader
    model, processor = download_or_load_clip_model()
    
    # Create embeddings directory if it doesn't exist
    print("Creating embeddings directory...")
    embeddings_dir = os.getenv("EMBEDDINGS_DIR", "embeddings")
    os.makedirs(embeddings_dir, exist_ok=True)
    
    # Get images from the specified directory
    print("Getting images from directory...")
    if os.getenv("TESTING") == "1":
        images_dir = os.getenv("TEST_IMAGES_DIR")
    else:
        images_dir = os.getenv("IMAGES_DIR")
    image_files = [p for p in Path(images_dir).glob("*") if p.suffix.lower() in ['.jpg', '.jpeg', '.png']]
    
    # Check if there are no images and return early if so
    if not image_files:
        print(f"No images found in directory: {images_dir}")
        return
    
    # Create a single CSV file for all embeddings
    embeddings_file = Path(embeddings_dir) / "image_embeddings.csv"
    
    # Check if the embeddings file already exists
    existing_processed_images = set()
    if embeddings_file.exists():
        print(f"Embeddings file already exists: {embeddings_file}")
        with open(embeddings_file, 'r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip header row
            for row in reader:
                if row:  # Skip empty rows
                    existing_processed_images.add(row[0])  # First column is the image path
    
    # Open the CSV file in append mode if it exists, or write mode if it doesn't
    file_mode = 'a' if embeddings_file.exists() else 'w'
    with open(embeddings_file, file_mode, newline='') as f:
        writer = csv.writer(f)
        
        # Write header row if creating a new file
        if file_mode == 'w':
            writer.writerow(["image_path", "embedding"])
        
        # Process each image and save its embedding
        for image_path in image_files:
            # Skip if image already processed
            if str(image_path) in existing_processed_images:
                print(f"Embedding already exists for: {image_path}")
                continue
                
            # Process image
            print(f"Processing image: {image_path}")
            try:
                image = Image.open(image_path)
                inputs = processor(images=image, return_tensors="pt", padding=True)
                image_features = model.get_image_features(**inputs)
                embedding = image_features.detach().cpu().numpy().flatten()
                
                # Save embedding to CSV
                print(f"Saving embedding for: {image_path}")
                writer.writerow([str(image_path), embedding.tolist()])
                
                print(f"Saved embedding for: {image_path}")
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
    
    print(f"Created {len(image_files)} embeddings successfully!")

if __name__ == "__main__":
    create_embeddings() 