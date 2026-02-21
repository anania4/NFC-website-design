#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting deployment script for Render..."

# Step 1: Install dependencies
echo "Installing dependencies..."
pip install asgiref certifi charset-normalizer Django idna pillow python-decouple requests sqlparse tzdata urllib3
# Step 2: Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Step 3: Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Step 3.1: Seed finance data
echo "Seeding finance data..."
python manage.py seed_finance_data

# Step 3.2: Create superuser (requires env vars)
echo "Creating superuser..."
python manage.py createsuperuser --noinput || true

# Step 4: Verify database tables (for debugging)
echo "Verifying database tables..."
python manage.py dbshell <<EOF
.tables
EOF

echo "Deployment completed successfully on Render!"
