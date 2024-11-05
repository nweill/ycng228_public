#!/bin/bash

# Get the Cloud Run URL
SERVICE_URL=$(gcloud run services describe cats-dogs-classifier --platform managed --region northamerica-northeast1 --format 'value(status.url)')

# Test the endpoint
echo "Testing Cloud Run endpoint at $SERVICE_URL"
curl -X POST \
  -F "file=@test_image.jpg" \
  $SERVICE_URL/predict
