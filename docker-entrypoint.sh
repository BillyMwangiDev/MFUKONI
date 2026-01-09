#!/bin/bash
set -e

echo "=========================================="
echo "Mfukoni Finance Tracker - Docker Entrypoint"
echo "=========================================="

# Ensure data directory exists
mkdir -p /app/data/mfukoni.db

# Initialize RDBMS if data directory is empty
if [ ! -f /app/data/mfukoni.db/categories.json ]; then
    echo "Initializing custom RDBMS database..."
    cd /app
    python migrate_rdbms.py 2>/dev/null || echo "Migration completed or tables already exist"
fi

# Collect static files (if needed)
echo "Collecting static files..."
cd /app/mfukoni_web
python manage.py collectstatic --noinput 2>/dev/null || true

# Wait for any initialization to complete
echo "Starting Mfukoni Finance Tracker..."
echo "=========================================="

# Execute the command passed to the container
exec "$@"
