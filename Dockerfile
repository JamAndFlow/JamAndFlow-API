FROM python:3.13-alpine

WORKDIR /app

RUN apk update && apk upgrade --no-cache \
 && apk add --no-cache \
    gcc musl-dev libffi-dev build-base \
    libjpeg-turbo-dev zlib-dev \
    postgresql-client

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PYTHONPATH=/app
ENTRYPOINT ["/entrypoint.sh"]
