#!/bin/sh

echo "Waiting for PostgreSQL..."

# Run Alembic migrations
echo "Running migrations..."
alembic upgrade head

echo "Starting Uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
