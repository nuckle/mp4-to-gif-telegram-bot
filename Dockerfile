FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY src /app/src

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/main.py"]
