#!/bin/sh
# filepath: entrypoint.sh

# TODO
# Wait for the database to be ready (optional, for robustness)
# Can use a tool like 'wait-for-it' or 'pg_isready' for production

set -e

cd /app/app
# Wait for Postgres to be ready
echo "Waiting for postgres..."
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  sleep 1
done

echo "Postgres is ready!"

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
