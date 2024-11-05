# Deploying MLFlow on Google Cloud Platform
## Overview
This guide provides step-by-step instructions to deploy an MLFlow server on a Google Cloud Platform (GCP) Compute Engine instance using a provided script. The script handles the creation of the Docker image, setting up the environment, and deploying MLFlow on a Compute Engine instance with a GCP bucket as the artifact store.

## Prerequisites
Before you begin, ensure you have the following:

- Google Cloud SDK installed and configured.
- Docker installed on your local machine.
- A Google Cloud Project with billing enabled.
- Basic knowledge of Docker and GCP.


## Step 1: Update the Deployment Script
Edit the Deployment Script:

Open the deploy_mlflow.sh script and update the BUCKET_NAME variable with the desired bucket name.
Ensure that the bucket name is unique across GCP and adheres to the naming conventions.
Create the Dockerfile:

Open the Dockerfile and update the --default-artifact-root parameter to point to your GCP bucket. For example:
```Dockerfile
CMD ["--backend-store-uri", "sqlite:///mlflow.db", "--default-artifact-root", "gs://<YOUR_BUCKET_NAME>/mlruns"]
```
Replace <YOUR_BUCKET_NAME> with the bucket name you set in the script.

## Step 2: Run the Deployment Script
### Make the Script Executable:

```bash
chmod +x deploy_mlflow.sh
```
### Run the script to create the GCP Compute Engine instance, set up the environment, and start the MLFlow server with the bucket as the artifact store:

```bash
./deploy_mlflow.sh
```
### Monitor the Deployment:
The script will display progress as it performs each step. If any errors occur, the script will stop and display a message.

## Step 3: Access MLFlow on GCP
### Get the External IP of the Instance:

At the end of the script execution, it will output the external IP address of your instance and the URL to access the MLFlow server:

```bash
MLFlow server is running. Access it at http://[EXTERNAL_IP]:5000
```
### Access MLFlow:

Open your browser and navigate to the provided URL.

## Step 4: Manage and Monitor Your Instance
### SSH into the Instance:

Access the instance via SSH:

```bash
gcloud compute ssh mlflow-instance --zone=us-west1-a
```
### Stopping/Starting the Instance:

Stop or start the instance with the following commands:

```bash
gcloud compute instances stop mlflow-instance --zone=us-west1-a
gcloud compute instances start mlflow-instance --zone=us-west1-a
```
### Delete the Instance (when no longer needed):

```bash
gcloud compute instances delete mlflow-instance --zone=us-west1-a
```

## Notes
Ensure that the bucket name in the script and Dockerfile matches.