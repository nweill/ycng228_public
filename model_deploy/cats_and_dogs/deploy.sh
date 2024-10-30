#!/bin/bash

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
PROJECT_ID=$(gcloud config get-value project)

# Build the image using Google Cloud Build
gcloud builds submit --tag gcr.io/$PROJECT_ID/cats-dogs-classifier .

# Deploy to Cloud Run with increased memory
gcloud run deploy cats-dogs-classifier \
  --image gcr.io/$PROJECT_ID/cats-dogs-classifier \
  --platform managed \
  --region northamerica-northeast1 \
  --allow-unauthenticated \
  --memory 1Gi

echo "Deployment complete!" 
