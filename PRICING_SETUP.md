# Dynamic Card Pricing Setup Guide

This guide explains how to set up and manage dynamic card pricing from the Django admin panel.

## Setup Instructions

### 1. Run Migrations

First, activate your virtual environment and run the migration to create the CardPricing table:

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Run migrations
python manage.py migrate
```

### 2. Populate Initial Pricing Data

Run the management command to populate the database with initial pricing:

```bash
python manage.py populate_pricing
```

This will create 4 pricing plans:
- Individual: 3,900 Birr (Most Popular)
- S&M Business: 3,600 Birr
- Enterprise: 3,200 Birr
- Corporate: 2,500 Birr (Best Value)

### 3. Access Admin Panel

1. Make sure you have a superuser account:
   ```bash
   python manage.py createsuperuser
   ```

2. Start the development server:
   ```bash
   python manage.py runserver
   ```

3. Navigate to: `http://127.0.0.1:8000/admin/`

4. Log in with your superuser credentials

5. Click on "Card Pricing" in the Checkout section

## Managing Pricing from Admin Panel

### Editing Existing Plans

1. Go to Admin Panel → Checkout → Card Pricing
2. Click on any plan to edit
3. You can modify:
   - **Name**: Display name (e.g., "Individual")
   - **Subtitle**: Short description (e.g., "Perfect for professionals")
   - **Price**: Price in Birr (e.g., 3900.00)
   - **Card Range**: Number of cards (e.g., "1-9 Cards")
   - **Features**: One feature per line (e.g., "Customized Design")
   - **Is Featured**: Show "Best Value" badge
   - **Is Popular**: Show "Most Popular" badge
   - **Display Order**: Order to display (lower numbers first)
   - **Is Active**: Show/hide this plan on the website

### Adding New Plans

1. Click "Add Card Pricing" button
2. Select a plan type from the dropdown
3. Fill in all required fields
4. Set display order (determines position on page)
5. Choose badges (Popular/Featured)
6. Click "Save"

### Features Field Format

Enter features one per line in the "Features" field:

```
Customized Design
2 Year Subscription
Digital Profile
Analytics Dashboard
Priority Support
```

### Display Order

Plans are displayed in ascending order by the "Display Order" field:
- Display Order 1 = First position (leftmost)
- Display Order 2 = Second position
- Display Order 3 = Third position
- Display Order 4 = Fourth position (rightmost)

### Badges

- **Most Popular**: Set "Is Popular" to True
- **Best Value**: Set "Is Featured" to True
- Only one badge will show per plan (Popular takes priority)

### Hiding Plans

To temporarily hide a plan without deleting it:
1. Edit the plan
2. Uncheck "Is Active"
3. Save

The plan will no longer appear on the website but remains in the database.

## How It Works

### Frontend Display

The card_detail.html template now dynamically loads pricing from the database:

```django
{% for plan in pricing_plans %}
<div class="card-type-box {% if plan.is_featured %}featured{% endif %}">
    {% if plan.is_popular %}
    <div class="card-badge">Most Popular</div>
    {% elif plan.is_featured %}
    <div class="card-badge">Best Value</div>
    {% endif %}
    
    <h2>{{ plan.name }}</h2>
    <p class="card-subtitle">{{ plan.subtitle }}</p>
    <div class="card-price">{{ plan.price|floatformat:0 }} <span>Birr</span></div>
    
    <ul class="card-features">
        <li>{{ plan.card_range }}</li>
        {% for feature in plan.get_features_list %}
        <li>{{ feature }}</li>
        {% endfor %}
    </ul>
    
    <a href="{% url 'checkout' %}?plan={{ plan.plan_type }}" class="card-cta-btn">Get Started</a>
</div>
{% endfor %}
```

### Backend Logic

The `CardDetailView` in `checkout/views.py` fetches active pricing plans:

```python
def get(self, request):
    pricing_plans = CardPricing.objects.filter(is_active=True).order_by('display_order')
    context = {'pricing_plans': pricing_plans}
    return render(request, 'card_detail.html', context)
```

## Database Model

The `CardPricing` model includes:

- `plan_type`: Unique identifier (individual, sm_business, enterprise, corporate)
- `name`: Display name
- `subtitle`: Short description
- `price`: Decimal field for price in Birr
- `card_range`: Text describing card quantity
- `features`: Multi-line text field for features
- `is_featured`: Boolean for "Best Value" badge
- `is_popular`: Boolean for "Most Popular" badge
- `display_order`: Integer for ordering
- `is_active`: Boolean to show/hide plan
- `created_at`: Timestamp
- `updated_at`: Timestamp

## Tips

1. **Pricing Updates**: Changes in the admin panel are reflected immediately on the website
2. **Backup**: Before making major changes, consider backing up your database
3. **Testing**: Test pricing changes on a staging environment first
4. **Consistency**: Keep feature lists consistent across plans for better comparison
5. **Mobile**: The grid automatically adjusts to 1 column on mobile devices

## Troubleshooting

### Plans Not Showing

1. Check if plans are marked as "Is Active" in admin
2. Verify the server is running
3. Clear browser cache
4. Check for JavaScript errors in browser console

### Migration Issues

If you encounter migration errors:

```bash
python manage.py migrate --run-syncdb
```

### Re-populate Data

To reset pricing to defaults:

```bash
python manage.py populate_pricing
```

This will update existing plans without creating duplicates.

## Support

For issues or questions, contact the development team or refer to the main README.md file.
