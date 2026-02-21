#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting deployment script for Render..."

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

# Step 4: Verify database tables (for debugging)
echo "Verifying database tables..."
python manage.py dbshell <<EOF
.tables
EOF

echo "Deployment completed successfully on Render!"
