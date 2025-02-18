#!/bin/sh

# echo "Applying database migrations..."
# python dongi/manage.py migrate

# echo "Collecting static files..."
# python dongi/manage.py collectstatic --noinput

echo "Starting Django server..."
exec "$@"
