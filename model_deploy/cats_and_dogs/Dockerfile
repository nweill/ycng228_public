# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PORT=8080
ENV PYTHONPATH=/app

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files
COPY requirements.txt .
COPY get_and_predict.py .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the FastAPI server
CMD ["python", "-m", "uvicorn", "get_and_predict:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1", "--timeout-keep-alive", "75"]
