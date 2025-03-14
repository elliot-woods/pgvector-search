import os
import csv
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
import ast

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

def store_embeddings():
    # Connect to database
    print("Connecting to database...")
    conn = get_db_connection()
    cur = conn.cursor()
    db_name = os.getenv("DB_NAME")
    
    # Get embeddings from the single CSV file
    print("Reading embeddings from disk...")
    embeddings_dir = os.getenv("EMBEDDINGS_DIR", "embeddings")
    embeddings_file = Path(embeddings_dir) / "image_embeddings.csv"
    
    if not embeddings_file.exists():
        print(f"Error: Embeddings file not found: {embeddings_file}")
        return
    
    
    # Read the embeddings from the CSV file
    print(f"Reading embeddings from: {embeddings_file}")
    count = 0
    
    try:
        with open(embeddings_file, 'r', newline='') as f:
            reader = csv.reader(f)
            
            for row in reader:
                if not row:  # Skip empty rows
                    continue
                    
                image_path = row[0]
                
                # Convert string representation of list to actual list
                embedding_str = row[1]
                try:
                    # Parse the string representation of the list
                    embedding_values = ast.literal_eval(embedding_str)
                    
                    # Store in database
                    print(f"Storing in database: {image_path}")
                    cur.execute(
                        f"INSERT INTO {db_name} (path, embedding) VALUES (%s, %s) ON CONFLICT (path) DO UPDATE SET embedding = EXCLUDED.embedding",
                        (image_path, embedding_values)
                    )
                    count += 1
                    
                except Exception as e:
                    print(f"Error processing embedding for {image_path}: {e}")
    
    except Exception as e:
        print(f"Error reading embeddings file: {e}")
    
    # Commit changes and close connection
    conn.commit()
    print(f"Committed {count} new embeddings to database")
    cur.close()
    conn.close()

if __name__ == "__main__":
    store_embeddings() 