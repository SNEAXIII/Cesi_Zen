FROM python:3.12-alpine

LABEL maintainer="SNEAXIII <misterbalise2@gmail.com>"

# Required to run wait for it
RUN apk add --no-cache bash

WORKDIR /app

RUN addgroup --system --gid 1001 python&&\
    adduser --system --uid 1001 fastapi

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chmod=755 --chown=fastapi:python migrations ./migrations
COPY --chmod=755 --chown=fastapi:python alembic.ini main.py run.sh wait-for-it.sh ./
COPY --chmod=755 --chown=fastapi:python src ./src
RUN find . -type f -name "*.sh" -exec dos2unix {} \;

USER fastapi