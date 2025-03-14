#!/bin/bash
set -e

# Load environment variables
if [ -f .env ]; then
    # Use a more robust way to load environment variables
    while IFS='=' read -r key value || [ -n "$key" ]; do
        # Skip comments and empty lines
        [[ $key =~ ^#.*$ || -z $key ]] && continue
        # Trim leading/trailing whitespace from value
        value=$(echo "$value" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
        # Export the variable
        export "$key=$value"
    done < .env
fi

# Check if required environment variables are set
if [ -z "$IMAGES_DIR" ]; then
    echo "Error: IMAGES_DIR environment variable is not set"
    exit 1
fi

if [ -z "$R2_BUCKET_NAME" ]; then
    echo "Error: R2_BUCKET_NAME environment variable is not set"
    exit 1
fi

if [ -z "$R2_ENDPOINT_URL" ]; then
    echo "Error: R2_ENDPOINT_URL environment variable is not set"
    exit 1
fi

if [ -z "$R2_ACCESS_KEY_ID" ] || [ -z "$R2_SECRET_ACCESS_KEY" ]; then
    echo "Error: R2 credentials are not set in environment variables"
    exit 1
fi

# Create the images directory if it doesn't exist
mkdir -p "$IMAGES_DIR"

echo "Downloading images from R2 bucket: $R2_BUCKET_NAME to $IMAGES_DIR"

# Set AWS credentials for this session
export AWS_ACCESS_KEY_ID="$R2_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="$R2_SECRET_ACCESS_KEY"

# Check if MAX_IMAGES is set
if [ -n "$MAX_IMAGES" ] && [ "$MAX_IMAGES" -gt 0 ]; then
    echo "Limiting download to $MAX_IMAGES images"
    
    # Get a list of image files from the bucket
    aws s3 ls "s3://$R2_BUCKET_NAME" --recursive --endpoint-url "$R2_ENDPOINT_URL" | \
        grep -E '\.jpg$|\.jpeg$|\.png$' | \
        awk '{print $4}' | \
        head -n "$MAX_IMAGES" > /tmp/image_list.txt
    
    # Download only the files in the list
    while IFS= read -r file; do
        aws s3 cp "s3://$R2_BUCKET_NAME/$file" "$IMAGES_DIR/$(basename "$file")" \
            --endpoint-url "$R2_ENDPOINT_URL" --only-show-errors
    done < /tmp/image_list.txt
    
    rm /tmp/image_list.txt
else
    # Use AWS CLI to download all images from R2 bucket
    aws s3 sync "s3://$R2_BUCKET_NAME" "$IMAGES_DIR" \
        --endpoint-url "$R2_ENDPOINT_URL" \
        --only-show-errors \
        --exclude "*" \
        --include "*.jpg" \
        --include "*.jpeg" \
        --include "*.png"
fi

# Count the number of downloaded images
image_count=$(find "$IMAGES_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) | wc -l)
echo "Successfully downloaded $image_count images to $IMAGES_DIR" 