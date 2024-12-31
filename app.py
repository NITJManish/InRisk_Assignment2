from flask import Flask, request, jsonify
from google.cloud import storage
import requests
import os
import json
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Google Cloud Storage bucket configuration
GCS_BUCKET_NAME = "your-gcs-bucket-name"
GCS_CLIENT = storage.Client()
BUCKET = GCS_CLIENT.bucket(GCS_BUCKET_NAME)

# Open-Meteo API base URL
OPEN_METEO_BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

# POST /store-weather-data
@app.route("/store-weather-data", methods=["POST"])
def store_weather_data():
    try:
        data = request.json
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        # Validate input
        if not all([latitude, longitude, start_date, end_date]):
            return jsonify({"error": "All fields (latitude, longitude, start_date, end_date) are required."}), 400

        # Fetch data from Open-Meteo API
        response = requests.get(OPEN_METEO_BASE_URL, params={
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "temperature_2m_mean",
                "apparent_temperature_max",
                "apparent_temperature_min",
                "apparent_temperature_mean"
            ],
            "timezone": "auto"
        })

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data from Open-Meteo API."}), response.status_code

        weather_data = response.json()

        # Generate file name based on current timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"weather_data_{latitude}_{longitude}_{start_date}_{end_date}_{timestamp}.json"

        # Save data to GCS
        blob = BUCKET.blob(file_name)
        blob.upload_from_string(json.dumps(weather_data), content_type="application/json")

        return jsonify({"message": "Weather data stored successfully.", "file_name": file_name}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET /list-weather-files
@app.route("/list-weather-files", methods=["GET"])
def list_weather_files():
    try:
        blobs = BUCKET.list_blobs()
        file_names = [blob.name for blob in blobs]
        return jsonify({"files": file_names}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET /weather-file-content/<file_name>
@app.route("/weather-file-content/<file_name>", methods=["GET"])
def get_weather_file_content(file_name):
    try:
        blob = BUCKET.blob(file_name)

        if not blob.exists():
            return jsonify({"error": "File not found."}), 404

        file_content = blob.download_as_text()
        return jsonify(json.loads(file_content)), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")

    app.run(host="0.0.0.0", port=8080)

