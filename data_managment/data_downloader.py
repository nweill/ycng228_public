import yfinance as yf
from google.cloud import storage
from datetime import datetime, timedelta
import os
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Set up the Google Cloud Storage client
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    logging.info(f"Uploading {source_file_name} to Google Cloud Storage bucket {bucket_name}...")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    logging.info(f"File {source_file_name} uploaded to {destination_blob_name}.")


# Fetch SP500 tickers
def fetch_sp500_tickers():
    logging.info("Fetching SP500 tickers...")

    # Example subset of SP500 tickers
    sp500_tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'BRK-B', 'JNJ', 'V', 'NVDA']

    logging.info(f"Fetched {len(sp500_tickers)} tickers.")
    return sp500_tickers


# Fetch historical data for a single day
def fetch_historical_data_for_day(tickers, day):
    logging.info(f"Fetching historical data for {day}...")
    end_date = day + timedelta(days=1)
    data = yf.download(tickers, start=day.date(), end=end_date.date())
    return data


# Determine the last pull date based on existing files in GCS or local folder
def get_last_pull_date(bucket_name=None, prefix=None, local_folder=None):
    last_date = None

    if local_folder:
        logging.info(f"Checking local folder {local_folder} for the last pull date...")
        files = os.listdir(local_folder)
        for file_name in files:
            if file_name.startswith('sp500_') and file_name.endswith('.csv'):
                date_str = file_name.split('_')[1].split('.')[0]
                date = datetime.strptime(date_str, '%Y-%m-%d')
                if last_date is None or date > last_date:
                    last_date = date
    else:
        logging.info(f"Checking Google Cloud Storage bucket {bucket_name} for the last pull date...")
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)
        for blob in blobs:

            date_str = blob.name.split('_')[-1].split('.')[0]
            date = datetime.strptime(date_str, '%Y-%m-%d')
            if last_date is None or date > last_date:
                last_date = date

    return last_date


# Check if a date is a weekday
def is_weekday(date):
    return date.weekday() < 5  # Monday to Friday are 0-4


def determine_start_date(last_pull_date, days):
    # Calculate the start date based on the days requested
    calculated_start_date = datetime.today() - timedelta(days=days)

    if last_pull_date:
        # Start from the latest date between the last pull date and the calculated start date
        start_date = max(last_pull_date + timedelta(days=1), calculated_start_date)
    else:
        # If no previous data, start from the calculated start date
        start_date = calculated_start_date

    # Adjust start_date to the closest valid weekday (not a weekend)
    while not is_weekday(start_date):
        start_date += timedelta(days=1)

    return start_date


# Main function to pull data and upload to GCS or local folder
def download_data_for(local_folder, days, bucket_name, prefix):

    if local_folder:
        # Check if the local folder exists, and create it if it doesn't
        if not os.path.exists(local_folder):
            logging.info(f"Local folder {local_folder} does not exist. Creating it...")
            os.makedirs(local_folder)
            logging.info(f"Local folder {local_folder} created.")

    # Get the last pull date
    last_pull_date = get_last_pull_date(bucket_name=bucket_name if not local_folder else None,
                                        prefix=prefix if not local_folder else None,
                                        local_folder=local_folder)

    # Determine the correct start date based on the last pull date or the specified number of days
    start_date = determine_start_date(last_pull_date, days)
    today = datetime.today()

    # Fetch SP500 tickers
    tickers = fetch_sp500_tickers()

    # Iterate over each day from start_date to today
    while start_date <= today:
        if not is_weekday(start_date):
            start_date += timedelta(days=1)
            continue

        # Fetch historical data for the current day
        data = fetch_historical_data_for_day(tickers, start_date)

        # Check if data is empty
        if data.empty:
            logging.info(f"No new data available for {start_date.strftime('%Y-%m-%d')}.")
        else:
            # Check if data has already been downloaded
            file_name = f"sp500_{start_date.strftime('%Y-%m-%d')}.csv"
            existing_files = os.listdir(local_folder) if local_folder else []
            if file_name in existing_files:
                logging.info(f"Data for {start_date.strftime('%Y-%m-%d')} has already been downloaded.")
            else:
                # Store data in CSV file
                data.to_csv(file_name)
                logging.info(f"Data stored in {file_name}.")

                if local_folder:
                    # Move the file to the local folder
                    destination_path = os.path.join(local_folder, file_name)
                    os.rename(file_name, destination_path)
                    logging.info(f"File moved to local folder: {destination_path}.")
                else:
                    # Upload to Google Cloud Storage
                    destination_blob_name = f"{prefix}{file_name}"
                    upload_to_gcs(bucket_name, file_name, destination_blob_name)
                    # Clean up the local file
                    os.remove(file_name)
                    logging.info(f"Local file {file_name} deleted.")

        # Move to the next day
        start_date += timedelta(days=1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch SP500 data and store it.')
    parser.add_argument('--local', type=str,
                        help='Local folder to store data. If used, checks this folder for the last pull date.')
    parser.add_argument('--days', type=int, help='Number of days of data to fetch.', required=True)
    args = parser.parse_args()

    bucket_name = 'ycng-sp500-bucket-nw'  # Replace with your bucket name
    prefix = 'daily_sp500_dumps/'
    local_folder = args.local
    days = args.days
    download_data_for(local_folder, days, bucket_name=bucket_name, prefix=prefix)
