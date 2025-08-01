FROM python:3.12-slim
LABEL maintainer="SNEAXIII <misterbalise2@gmail.com>"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .