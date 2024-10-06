from flask import Flask, request
from azure.communication.email import EmailClient

from dotenv import load_dotenv
import os

app = Flask(__name__)

# Configuration from environment variables
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")


def send_email(subject, body, html_body):
    try:
        print("trying to send message")
        connection_string = EMAIL_PASSWORD
        client = EmailClient.from_connection_string(connection_string)

        message = {
            "senderAddress": EMAIL_USER,
            "recipients": {"to": [{"address": EMAIL_RECEIVER}]},
            "content": {
                "subject": subject,
                "plainText": body,
                "html": """
				<html>
					<body>
						"""
                + html_body
                + """
					</body>
				</html>""",
            },
        }

        poller = client.begin_send(message)
        result = poller.result()
        print("Message sent: ", result.message_id)

    except Exception as ex:
        print(ex)


@app.route("/send_abnormal_email", methods=["POST"])
def send_abnormal_email():
    print("Sending abnormal email")
    data = request.json
    subject = data["subject"]
    download_link = data["download_link"]
    body = f"An abnormal quake was detected. Download the data here: {download_link}"
    html_body = f"An abnormal quake was detected. Download the data here: <a href={download_link}>{download_link}</a>"
    send_email(subject, body, html_body)
    return {"message": "Abnormal quake email sent"}, 200


@app.route("/send_normal_email", methods=["POST"])
def send_normal_email():
    data = request.json
    subject = data["subject"]
    download_link = data["download_link"]
    body = f"A new quake was detected. Download the data here: {download_link}"
    html_body = f"A new quake was detected. Download the data here: <a href={download_link}>{download_link}</a>"
    send_email(subject, body, html_body)
    return {"message": "Normal quake email sent"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
