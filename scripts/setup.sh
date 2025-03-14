#!/bin/bash
set -e

# Main setup script that runs both database setup and embedding creation

# Step 1: Set up the database
echo "Step 1: Running database setup..."
chmod +x /app/scripts/setup_db.sh
/app/scripts/setup_db.sh

# Step 2: Create and store embeddings
echo "Step 2: Running embeddings setup..."
chmod +x /app/scripts/setup_embeddings.sh
/app/scripts/setup_embeddings.sh

# Step 3: Create embedding index after embeddings have been loaded
echo "Step 3: Creating embedding index in database..."
chmod +x /app/scripts/setup_embedding_index.sh
/app/scripts/setup_embedding_index.sh

echo "Setup complete!"
