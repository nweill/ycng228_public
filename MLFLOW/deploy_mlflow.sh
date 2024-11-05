#!/bin/bash

# Set variables
INSTANCE_NAME="mlflow-instance"
ZONE="us-west1-a"
MACHINE_TYPE="e2-medium"
IMAGE_FAMILY="debian-11"
IMAGE_PROJECT="debian-cloud"
BOOT_DISK_SIZE="20GB"
DOCKERFILE_PATH="./Dockerfile"
FIREWALL_RULE_NAME="allow-http-mlflow"
TAGS="http-server"
BUCKET_NAME="XXX"  # Set your desired bucket name here

# Step 1: Create a GCP Compute Engine Instance with the http-server tag
echo "Creating Google Cloud Compute Engine instance..."
gcloud compute instances create $INSTANCE_NAME \
    --machine-type=$MACHINE_TYPE \
    --image-family=$IMAGE_FAMILY \
    --image-project=$IMAGE_PROJECT \
    --boot-disk-size=$BOOT_DISK_SIZE \
    --zone=$ZONE \
    --tags=$TAGS

if [ $? -ne 0 ]; then
    echo "Failed to create instance. Please check your settings."
    exit 1
fi

# Step 2: Create a GCS bucket for storing MLFlow artifacts
echo "Creating GCS bucket for MLFlow artifacts..."
gsutil mb -l us-west1 gs://$BUCKET_NAME/

if [ $? -ne 0 ]; then
    echo "Failed to create GCS bucket. Please check your settings."
    exit 1
fi

# Step 3: Assign necessary IAM permissions to the Compute Engine instance
echo "Assigning storage admin role to the Compute Engine service account..."
SERVICE_ACCOUNT=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format='get(serviceAccounts[0].email)')
gcloud projects add-iam-policy-binding $(gcloud config get-value project) \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $(gcloud config get-value project) \
    --member="user:$(gcloud config get-value account)" \
    --role="roles/storage.admin"

if [ $? -ne 0 ]; then
    echo "Failed to assign IAM role. Please check your settings."
    exit 1
fi

# Step 4: Create a firewall rule to allow HTTP traffic on port 5000
echo "Creating firewall rule to allow HTTP traffic on port 5000..."
gcloud compute firewall-rules create $FIREWALL_RULE_NAME \
    --allow tcp:5000 \
    --target-tags=$TAGS \
    --description="Allow port 5000 for MLFlow" \
    --direction=INGRESS || echo "Firewall rule already exists, skipping creation."

# Step 5: Wait for SSH to be available
echo "Waiting for SSH to be available..."
while ! gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command="echo SSH is ready"; do
    echo "SSH not ready, waiting..."
    sleep 10
done

# Step 6: Install Docker on the Instance
echo "Installing Docker on the instance..."
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command="\
    sudo apt-get update && \
    sudo apt-get install -y docker.io && \
    sudo systemctl start docker && \
    sudo systemctl enable docker && \
    sudo usermod -aG docker \$USER \
"

if [ $? -ne 0 ]; then
    echo "Failed to install Docker. Please check the instance and try again."
    exit 1
fi

# Step 7: Upload the Dockerfile
echo "Uploading Dockerfile to the instance..."
gcloud compute scp $DOCKERFILE_PATH $INSTANCE_NAME:~/Dockerfile --zone=$ZONE

if [ $? -ne 0 ]; then
    echo "Failed to upload Dockerfile. Please check your file path and try again."
    exit 1
fi

# Step 8: Build the Docker Image on the Instance
echo "Building the Docker image on the instance..."
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command="\
    docker build -t mlflow-image:latest -f Dockerfile . \
"

if [ $? -ne 0 ]; then
    echo "Failed to build Docker image. Please check the Dockerfile and logs."
    exit 1
fi

# Step 9: Run the Docker Container with GCS as the artifact store
echo "Running the Docker container with GCS as the artifact store..."
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command="\
    docker run -d -p 5000:5000 -v \$HOME:/app mlflow-image:latest
"

if [ $? -ne 0 ]; then
    echo "Failed to run Docker container. Please check the logs."
    exit 1
fi

# Step 10: Get the external IP address and output the access URL
EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
echo "MLFlow server is running. Access it at http://$EXTERNAL_IP:5000"

echo "Deployment complete."
