# SP500 Data Downloader Script

## Overview

This Python script downloads historical SP500 stock data using the `yfinance` library. It fetches data for a specified number of days, stores it either locally or in a Google Cloud Storage (GCS) bucket, and ensures that the data is not re-downloaded if it already exists.

## Prerequisites

Before running the script, ensure that you have followed the steps described in setup.md.

## Script Arguments
`--local`: (Optional) Specify a local directory to store the downloaded data. If omitted, the data will be uploaded to Google Cloud Storage.

`--days`: (Required) The number of days of data to fetch, counting backward from today.

### Usage

**Example 1**: Store Data Locally

To download the last 10 days of SP500 data and store it in a local directory named data:

```bash
python data_downloader.py --local data --days 10
```
This command will:

- Create the data directory if it doesn't exist.
- Check the directory for the last pulled date.
- Download data from the most recent date not already downloaded, up to 10 days ago.
- Save each day's data as a separate CSV file named sp500_YYYY-MM-DD.csv in the data directory.


**Example 2**: Store Data in Google Cloud Storage
To download the last 10 days of SP500 data and store it in a Google Cloud Storage bucket:

```bash
python data_downloader.py --days 10
```
This command will:
- Check the specified GCS bucket for the last pulled date.
- Download data from the most recent date not already downloaded, up to 10 days ago.
- Save each day's data as a separate CSV file named sp500_YYYY-MM-DD.csv in the specified GCS bucket.

### Handling Authentication
For Google Cloud Storage, ensure that your environment is authenticated with Google Cloud using the following command:

```bash
gcloud auth application-default login
```
This will set up the necessary credentials for the script to interact with Google Cloud Storage.

### Logging
The script uses Python's built-in logging module to log its activities. Logs will be printed to the console, showing progress and any issues encountered during execution.

## Additional Notes
**Weekend Data**: The script skips weekends automatically, so no data will be fetched for Saturdays or Sundays.

**Existing Data**: If the data for a particular day already exists in the target directory or GCS bucket, the script will skip downloading that day's data.

By following these instructions, you should be able to use the script effectively to download and manage SP500 data.