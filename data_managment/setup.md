# Google Cloud Setup Instructions

## Overview

This guide will help you set up a new Google Cloud account using a fresh Google email address. By following these steps, you'll gain access to Google Cloud's free tier, which includes Google Cloud Storage. This is essential for storing and managing the SP500 data as part of our MLOps course.

## Steps to Set Up Google Cloud and Enable Cloud Storage

### 1. Create a New Google Email Account

1. Visit [Google Account Creation](https://accounts.google.com/signup).
2. Fill in the required details to create a new Google account.
   - First name, Last name
   - Choose a fresh username (Gmail address)
   - Create a strong password
3. Click on "Next" and follow the instructions to verify your account (you may need a phone number for verification).
4. Once verified, you'll be redirected to your new Gmail inbox.

### 2. Sign Up for Google Cloud

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Click on "Get started for free."
3. Sign in with your newly created Google account.
4. You'll be prompted to sign up for the Google Cloud Free Tier. The free tier includes $300 in free credits and free usage of some resources like Google Cloud Storage for 90 days.
   - Enter your details, including your billing information (Google Cloud requires a credit card, but you won’t be charged unless you exceed the free tier limits).
   - Agree to the terms and conditions, then click "Start my free trial."

### 3. Enable Google Cloud Storage

1. Once in the Google Cloud Console, you'll see a dashboard.
2. Use the search bar at the top and search for "Cloud Storage."
3. Click on "Cloud Storage" in the search results to open the Cloud Storage console.
4. You’ll be prompted to create a project if you don’t have one already:
   - Click "Create Project."
   - Give your project a name (e.g., `mlops-sp500-data`).
   - Click "Create."
5. With your project created, you can now enable Cloud Storage:
   - Click on "Create Bucket."
   - Name your bucket (e.g., `ycng-sp500-bucket_[your_name]`).
   - Choose a region close to your location for optimal performance.
   - Select "Standard" as the storage class.
   - Click "Create" to finalize your Cloud Storage bucket.

### 4. Install Google Cloud SDK and Authenticate

1. Download and install the Google Cloud SDK:
   - Visit [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) and follow the instructions for your operating system.
2. Once installed, open a terminal or command prompt and run the following command to authenticate:
   ```bash
   gcloud auth login
   

### 5. Enable Google Cloud Storage and Create a Bucket Using gcloud Commands

If you know your project ID and want to enable Cloud Storage and create a bucket via the command line, follow these steps:

1. **Set your project**:
   ```bash
   gcloud config set project [YOUR_PROJECT_ID]
   ```
   

2. **Enable the Cloud Storage service:**:
   ```bash
   gcloud services enable storage.googleapis.com
   ```
   

3. **Create a Cloud Storage bucket:**

```bash
gsutil mb -p [YOUR_PROJECT_ID] -l [REGION] gs://[YOUR_BUCKET_NAME]/
```

Replace [YOUR_PROJECT_ID] with your actual Google Cloud project ID.

Replace [REGION] with the desired region (e.g., us-central1).

Replace [YOUR_BUCKET_NAME] with your desired bucket name (e.g., ycng228-sp500-bucket_[your_name]).

4. **Allow the code to connect**

```bash
gcloud auth application-default login
```
