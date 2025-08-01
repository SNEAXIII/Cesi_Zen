FROM python:3.12-slim
LABEL maintainer="SNEAXIII <misterbalise2@gmail.com>"
RUN apt-get update && apt-get install -y dos2unix && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN find . -type f -name "*.sh" -exec dos2unix {} \;