#!/bin/bash

# Wait for database
echo "Waiting for database..."
until python -c "import psycopg2; psycopg2.connect(host='db', port=5432, user='cms_user', password='secure_password_123', dbname='cms_backend')" 2>/dev/null; do
  echo "Database not ready, waiting..."
  sleep 2
done
echo "Database started"

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start server
if [ "$1" = "celery" ]; then
    celery -A core worker --loglevel=info
elif [ "$1" = "celery-beat" ]; then
    celery -A core beat --loglevel=info
else
    gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi