# Include environment variables from .env file
include .env
export

.PHONY: build up up-detached down setup clean shell db start logs test-search-text


build:
	docker-compose build

shell:
	docker-compose exec api bash

db-shell:
	docker-compose exec db bash

up-detached:
	docker-compose up -d

db:
	docker-compose exec db bash -c "PGPASSWORD=$(DB_PASSWORD) psql -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME)"

down:
	docker-compose down

setup:
	docker-compose up -d db # Start DB container
	sleep 5  # Wait for DB to be ready
	docker-compose up -d api  # Start API container
	docker-compose exec api sh -c "chmod +x /app/scripts/setup.sh /app/scripts/setup_db.sh /app/scripts/setup_embeddings.sh /app/scripts/setup_embedding_index.sh && /app/scripts/setup.sh"
	@echo "Setup complete. API container is running in the background."

start: clean build up-detached setup
	@echo "Application started successfully in detached mode. Use 'make logs' to view logs."

logs:
	docker-compose logs -f

clean:
	docker-compose down -v

test-search-text:
	@echo "Testing /search-by-text with 'a boat' query and limit 5..."
	@curl -s -X GET "http://localhost:8000/search-by-text?query=a+boat&limit=5"
	@echo "Testing /search-by-text with 'a car' query and limit 5..."
	@curl -s -X GET "http://localhost:8000/search-by-text?query=a+car&limit=5"
	@echo "Testing /search-by-text with 'a green tree' query and limit 3..."
	@curl -s -X GET "http://localhost:8000/search-by-text?query=a+green+tree&limit=3"
	@echo "\nTest completed."
