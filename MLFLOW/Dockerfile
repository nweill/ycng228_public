# Use the official Python image as a base
FROM python:3.9-slim

# Set environment variables to avoid issues with input buffering
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install MLFlow and Google Cloud Storage dependencies
RUN pip install --no-cache-dir mlflow google-cloud-storage

# Make the working directory writable
RUN chmod -R 777 /app

# Expose the default MLFlow port
EXPOSE 5000

# Define the entrypoint for the MLFlow server
ENTRYPOINT ["mlflow", "server", "--host", "0.0.0.0"]

# Optionally specify default parameters for the MLFlow server
CMD ["--backend-store-uri", "sqlite:///mlflow.db", "--default-artifact-root", "gs://mlflow-artifacts-bucket-nw/mlruns"]
