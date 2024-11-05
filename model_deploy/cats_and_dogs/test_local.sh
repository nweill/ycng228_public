#!/bin/bash

# Build and run locally
echo "Building and running locally..."
docker build -t cats-dogs-classifier -f Dockerfile ..
docker run -p 8080:8080 cats-dogs-classifier &

# Wait for the container to start
echo "Waiting for container to start..."
sleep 10

# Download a sample image if test_image.jpg doesn't exist
if [ ! -f "test_image.jpg" ]; then
    echo "Downloading sample image..."
    curl -o test_image.jpg https://raw.githubusercontent.com/pytorch/hub/master/images/dog.jpg
fi

# Local test
echo "Testing locally..."
curl -X POST \
  -F "file=@test_image.jpg" \
  http://localhost:8080/predict

# Stop the container
echo "Stopping container..."
CONTAINER_ID=$(docker ps -q --filter ancestor=cats-dogs-classifier)
if [ ! -z "$CONTAINER_ID" ]; then
    docker stop $CONTAINER_ID
else
    echo "No container found to stop"
fi
