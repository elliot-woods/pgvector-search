#!/bin/bash

# This script refreshes the vector index after embeddings have been loaded
echo "Creating embedding index in database..."

# Drop existing index if it exists and recreate it
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME <<EOF
DROP INDEX IF EXISTS image_embedding_idx;
CREATE INDEX image_embedding_idx ON images USING ivfflat (embedding vector_cosine_ops);
VACUUM ANALYZE images;
EOF

echo "Embedding index created successfully!" 