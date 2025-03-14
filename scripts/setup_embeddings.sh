#!/bin/bash
set -e

# Create embeddings from images and save to disk
echo "Creating embeddings from images..."
python api/create_embeddings.py

# Store embeddings in the database
echo "Storing embeddings in the database..."
python api/store_embeddings.py

echo "Embedding process complete!" 
