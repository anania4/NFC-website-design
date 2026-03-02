#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting deployment script..."

# Step 1: Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
# Step 2: Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Step 3: Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Step 3.1: Seed finance data (if applicable)
echo "Seeding finance data..."
python manage.py seed_finance_data || echo "Seed command not found, skipping..."

# Step 3.2: Create superuser (requires env vars)
echo "Creating superuser..."
python manage.py createsuperuser --noinput || true

echo "Deployment completed successfully!"
