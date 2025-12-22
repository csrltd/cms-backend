#!/bin/bash
set -e

echo "Waiting for database..."

until python - <<EOF
import psycopg2
import os

psycopg2.connect(
    dbname=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=os.environ.get("DB_PORT", 5432),
)
EOF
do
  echo "Database not ready, waiting..."
  sleep 2
done

echo "Database started"

# Run migrations

python manage.py migrate account --noinput

# python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start server
if [ "$1" = "celery" ]; then
    celery -A core worker --loglevel=info
elif [ "$1" = "celery-beat" ]; then
    celery -A core beat --loglevel=info
else
    gunicorn core.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3
fi
