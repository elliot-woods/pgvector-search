#!/bin/bash


# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d postgres -c '\q'; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

# Create database and enable pgvector extension
echo "Creating database and enabling pgvector extension..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d postgres <<EOF
CREATE DATABASE $DB_NAME;
\c $DB_NAME
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    path TEXT UNIQUE NOT NULL,
    embedding vector(512),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index will be created after embeddings are loaded for better performance
-- CREATE INDEX IF NOT EXISTS image_embedding_idx ON images USING ivfflat (embedding vector_cosine_ops);
EOF

echo "Database setup complete!"

