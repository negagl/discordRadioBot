FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt update && apt install ffmpeg -y

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python3", "main.py"]
