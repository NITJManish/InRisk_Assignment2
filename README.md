## comment to run program
cmd : python app.py

# Weather Data Storage and Retrieval API

This is a Flask-based backend service that fetches historical weather data from the Open-Meteo API, stores the data in Google Cloud Storage (GCS), and provides APIs to list and retrieve the stored data.

## Features
- Fetch weather data for specific locations and date ranges.
- Store weather data as JSON files in a GCS bucket.
- List all stored weather data files.
- Retrieve the content of specific weather data files.

## Prerequisites
1. **Google Cloud Platform (GCP) Configuration:**
   - Set up a GCS bucket and note down the bucket name.
   - Create and download a service account key with storage access. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of the key file.

2. **Python Requirements:**
   - Python 3.8 or higher
   - Install the required dependencies using `pip`.


## API Endpoints
1. POST /store-weather-data
Fetches weather data from the Open-Meteo API and stores it in GCS.

2. GET /list-weather-files
Lists all stored weather data files in the GCS bucket.

3. GET /weather-file-content/<file_name
Retrieves the content of a specific JSON file stored in GCS.
![image](https://github.com/user-attachments/assets/29be74cf-617c-4d48-ba12-f01d0b2e1deb)

