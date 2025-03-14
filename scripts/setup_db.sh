#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d postgres -c '\q'; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

# Create database and enable pgvector extension
echo "Creating database and a table for embeddings with pgvector extension called $DB_NAME..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d postgres <<EOF
CREATE DATABASE $DB_NAME;
\c $DB_NAME
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS $DB_NAME (
    id SERIAL PRIMARY KEY,
    path TEXT UNIQUE NOT NULL,
    embedding vector(512),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
EOF

echo "Database setup complete!"

