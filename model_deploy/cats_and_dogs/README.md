# Cats and Dogs Classifier

This project is a FastAPI application that classifies images of cats and dogs using a pre-trained ResNet-50 model from torchvision. The application is containerized using Docker and can be deployed to Google Cloud Run.

## Prerequisites

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and configured
- [Docker](https://docs.docker.com/get-docker/) installed
- A Google Cloud project with billing enabled
- [Python 3.9](https://www.python.org/downloads/release/python-390/) installed

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd model_serving/cats_and_dogs
   ```

2. **Install dependencies locally** (optional, for local testing):
   ```bash
   pip install -r requirements.txt
   ```

## Local Testing

1. **Run the application locally**:
   ```bash
   uvicorn get_and_predict:app --host 0.0.0.0 --port 8080
   ```

2. **Test the endpoints**:
   - Health check: `GET http://localhost:8080/health`
   - Prediction: `POST http://localhost:8080/predict` with an image file

## Deployment to Google Cloud Run

1. **Build and deploy the application**:
   Run the `deploy.sh` script to build the Docker image and deploy it to Google Cloud Run:
   ```bash
   ./deploy.sh
   ```

2. **Access the deployed service**:
   After deployment, you will receive a URL for the service. Use this URL to access the health check and prediction endpoints.

## Scripts

- `deploy.sh`: Builds the Docker image using Google Cloud Build and deploys it to Google Cloud Run.
- `test_cloud_run.sh`: (Optional) Script to test the deployed service on Cloud Run.
- `test_local.sh`: (Optional) Script to test the application locally.

## Notes

- Ensure that the `requirements.txt` and `get_and_predict.py` files are in the same directory as the `Dockerfile` for the build process to work correctly.
- The application requires a memory limit of at least 1 GiB on Cloud Run due to the model size and processing requirements.

## Troubleshooting

- If the deployment fails, check the Google Cloud Run logs for more details.
- Ensure that the Google Cloud SDK is authenticated and configured to use the correct project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
