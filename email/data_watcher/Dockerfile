FROM python:3.9-slim

WORKDIR /app
COPY watcher.py requirements.txt ./
RUN pip install -r requirements.txt

CMD ["python", "watcher.py"]
