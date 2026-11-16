#!/bin/sh
set -e

echo "Menjalankan migrasi database..."
uv run python manage.py migrate --noinput

echo "Memulai server Gunicorn pada port ${PORT:-8000}..."
exec uv run gunicorn config.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers 3 \
    --access-logfile - \
    --error-logfile -
