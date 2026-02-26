#!/bin/bash
# Setup script for dynamic pricing feature

echo "=========================================="
echo "TAP Card Pricing Setup"
echo "=========================================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Virtual environment not activated"
    echo "Please activate your virtual environment first:"
    echo "  Windows: venv\\Scripts\\activate"
    echo "  macOS/Linux: source venv/bin/activate"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Step 1: Running migrations..."
python manage.py migrate

if [ $? -ne 0 ]; then
    echo "❌ Migration failed!"
    exit 1
fi

echo "✅ Migrations completed"
echo ""

echo "Step 2: Populating initial pricing data..."
python manage.py populate_pricing

if [ $? -ne 0 ]; then
    echo "❌ Failed to populate pricing!"
    exit 1
fi

echo "✅ Pricing data populated"
echo ""

echo "=========================================="
echo "Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Start the server: python manage.py runserver"
echo "2. Visit: http://127.0.0.1:8000/card-detail/"
echo "3. Manage pricing: http://127.0.0.1:8000/admin/"
echo ""
echo "For more information, see PRICING_SETUP.md"
echo ""
