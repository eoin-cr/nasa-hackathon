FROM python:3.9-slim

WORKDIR /app
COPY email_sender.py requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 5001
CMD ["python", "email_sender.py"]
