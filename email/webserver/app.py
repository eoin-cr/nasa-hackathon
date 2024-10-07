from flask import Flask, request, jsonify, send_from_directory
import os
import pandas as pd
import requests

app = Flask(__name__)

UPLOAD_FOLDER = "./data"
THRESHOLD_MULTIPLIER = 2.5
MEDIAN_VALUE = 5.473234895023897e-09
THRESHOLD_VALUE = MEDIAN_VALUE * THRESHOLD_MULTIPLIER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/upload", methods=["POST"])
def upload_data():
    file = request.files["file"]
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Load the CSV file and check max velocity
    df = pd.read_csv(file_path)
    max_velocity = df["velocity(m/s)"].max()
    min_velocity = df["velocity(m/s)"].min()

    max_abs_vel = max(abs(max_velocity), abs(min_velocity))
    if max_abs_vel > THRESHOLD_VALUE:
        # Trigger abnormal quake email
        email_service_url = "http://email_service:5001/send_abnormal_email"
        subject = f"Abnormal quake with max velocity {max_abs_vel/MEDIAN_VALUE:.2f}x bigger than median detected"
    else:
        # Trigger normal quake email
        email_service_url = "http://email_service:5001/send_normal_email"
        subject = "New quake detected"

    download_link = f"http://localhost:5000/download/{filename}"
    data = {"subject": subject, "download_link": download_link}
    requests.post(email_service_url, json=data)

    return jsonify({"message": "File received and processed"}), 200


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
