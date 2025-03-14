#!/bin/bash

# Create embeddings from images and save to disk
echo "Step 1: Creating embeddings from images..."
python app/create_embeddings.py

# Store embeddings in the database
echo "Step 2: Storing embeddings in the database..."
python app/store_embeddings.py

echo "Embedding process complete!" 
