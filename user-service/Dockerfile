FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y curl \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
