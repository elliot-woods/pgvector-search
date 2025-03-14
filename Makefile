# Include environment variables from .env file
include .env
export

# If TESTING is set to 1, the script will use the test images directory (TEST_IMAGES_DIR) to create embeddings
TESTING ?= 0

build:
	docker-compose build

up:
	docker-compose up -d db # Start DB container
	TESTING=$(TESTING) docker-compose up -d api # Start API container with TESTING env var

api-shell:
	docker-compose exec api bash

db-shell:
	docker-compose exec db bash -c "PGPASSWORD=$(DB_PASSWORD) psql -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME)"

setup:
	docker-compose exec -e TESTING=$(TESTING) api sh -c "/app/scripts/setup.sh" # Create embeddings and load them into a pg_vector table
	@echo "Setup complete. API container is running in the background."

download-images:
	@echo "Downloading images from R2 bucket to $(IMAGES_DIR)..."
	MAX_IMAGES=$(MAX_IMAGES) ./scripts/download_images.sh
	@echo "Image download complete."

logs:
	docker-compose logs -f

clean:
	rm -rf embeddings/*
	docker-compose down -v

start: clean build up setup logs
	@echo "Application started successfully in detached mode. Use 'make logs' to view logs."

test-api:
	@echo "Testing /search-by-text with '$(SEARCH)' query and limit $(LIMIT)..."
	@curl -s -X GET "http://localhost:8000/search-by-text?query=$(subst $(space),+,$(SEARCH))&limit=$(LIMIT)" | jq

# Define a variable for space to use in substitution
space := $(empty) $(empty)

.PHONY: build up api-shell db-shell setup logs clean start test-search-by-text download-images
