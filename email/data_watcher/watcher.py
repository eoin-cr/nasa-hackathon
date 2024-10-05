import os
import time
import requests

WATCHED_DIR = "/watched_dir"
FLASK_SERVER_URL = "http://webserver:5000/upload"


def process_file(file_path):
    filename = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        files = {"file": (filename, f)}
        response = requests.post(FLASK_SERVER_URL, files=files)

    if response.status_code == 200:
        print(f"Successfully uploaded {filename}")
        os.remove(file_path)
    else:
        print(f"Failed to upload {filename}")


def watch_directory():
    while True:
        for filename in os.listdir(WATCHED_DIR):
            file_path = os.path.join(WATCHED_DIR, filename)
            if os.path.isfile(file_path):
                process_file(file_path)
        time.sleep(5)


if __name__ == "__main__":
    watch_directory()
