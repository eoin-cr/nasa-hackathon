from flask import Flask, request
import smtplib
import os

app = Flask(__name__)

# Configuration from environment variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")


def send_email(subject, body):
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        message = f"Subject: {subject}\n\n{body}"
        smtp.sendmail(EMAIL_USER, EMAIL_RECEIVER, message)


@app.route("/send_abnormal_email", methods=["POST"])
def send_abnormal_email():
    data = request.json
    subject = data["subject"]
    download_link = data["download_link"]
    body = f"An abnormal quake was detected. Download the data here: {download_link}"
    send_email(subject, body)
    return {"message": "Abnormal quake email sent"}, 200


@app.route("/send_normal_email", methods=["POST"])
def send_normal_email():
    data = request.json
    subject = data["subject"]
    download_link = data["download_link"]
    body = f"A new quake was detected. Download the data here: {download_link}"
    send_email(subject, body)
    return {"message": "Normal quake email sent"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
