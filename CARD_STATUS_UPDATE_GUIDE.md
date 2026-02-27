# Card Status Real-Time Update System

## Overview

This system ensures that when you update card pricing information in the Django admin panel, all displays across the website automatically reflect the changes without requiring manual cache clearing or server restarts.

## How It Works

### 1. **Django Signals** (`checkout/signals.py`)
   - Automatically detects when a `CardPricing` record is created, updated, or deleted
   - Immediately invalidates the cached pricing data
   - Logs all cache invalidation events for monitoring

### 2. **Cache Layer** (`src/settings.py`)
   - Uses Django's local-memory cache (can be upgraded to Redis for production)
   - Stores active pricing plans for 1 hour (auto-invalidated on changes)
   - Reduces database queries and improves page load times

### 3. **Dynamic Views** (`checkout/views.py`)
   - `HomeView`: Displays pricing on the homepage
   - `CardDetailView`: Shows detailed pricing page
   - Both views check cache first, then database if cache is empty

### 4. **Dynamic Templates**
   - `templates/home.html`: Homepage pricing section now uses dynamic data
   - `templates/card_detail.html`: Already dynamic, now with caching

## Features

✅ **Automatic Updates**: Changes in admin panel instantly reflect on website
✅ **Performance**: Cached data reduces database load
✅ **Logging**: All cache operations are logged for debugging
✅ **Fallback**: If cache fails, data is fetched directly from database
✅ **Admin Control**: Full control over pricing via admin panel

## Admin Panel Usage

### Updating Card Pricing

1. Go to Django Admin: `/admin/`
2. Navigate to **Checkout** → **Card Pricing**
3. Click on any pricing plan to edit
4. Make your changes:
   - Update price
   - Change name or subtitle
   - Modify features
   - Toggle active status
   - Adjust display order
5. Click **Save**
6. **The website updates automatically!**

### Available Fields

- **Plan Type**: Unique identifier (e.g., 'individual', 'enterprise')
- **Name**: Display name (e.g., 'Individual Cards')
- **Subtitle**: Short description
- **Price**: Price in Birr
- **Card Range**: Quantity description (e.g., '<10', '10-25')
- **Features**: One feature per line
- **Is Featured**: Shows 'Best Value' badge
- **Is Popular**: Shows 'Most Popular' badge
- **Display Order**: Controls card order (lower = first)
- **Is Active**: Show/hide on website

## Testing

### Test Cache Invalidation

Run the test command:

```bash
python manage.py test_pricing_cache
```

This will:
- Show current cached data
- Display database data
- Clear the cache
- Confirm cache was cleared

### Manual Testing Steps

1. **View Current Pricing**
   - Visit homepage: `/`
   - Scroll to pricing section
   - Note current prices

2. **Update in Admin**
   - Go to `/admin/checkout/cardpricing/`
   - Edit any plan
   - Change the price
   - Save

3. **Verify Update**
   - Refresh homepage
   - New price should appear immediately
   - Check card detail page: `/card-detail/`
   - Price should match

### Check Logs

View cache invalidation logs:

```bash
# View all logs
cat logs/django.log | grep "CardPricing"

# View recent logs
tail -f logs/django.log
```

## Where Cards Are Displayed

1. **Homepage** (`/`)
   - Pricing section with dynamic cards
   - Dynamic data from database
   - Cached for performance

2. **Card Detail Page** (`/card-detail/`)
   - Detailed pricing grid
   - Shows all active plans
   - Includes features and badges

3. **Checkout Page** (`/checkout/`) ✨ NEW
   - Subscription type dropdown
   - Dynamic pricing calculation
   - Real-time price updates based on quantity

## Technical Details

### Cache Key
- Key: `'active_pricing_plans'`
- Timeout: 3600 seconds (1 hour)
- Auto-invalidated on model changes

### Signal Flow
```
Admin saves CardPricing
    ↓
post_save signal fires
    ↓
Cache invalidated
    ↓
Next page load fetches fresh data
    ↓
New data cached
```

### View Flow
```
User visits page
    ↓
View checks cache
    ↓
Cache hit? → Return cached data
    ↓
Cache miss? → Query database → Cache result → Return data
```

## Production Considerations

### Upgrade to Redis (Recommended)

For production, replace local-memory cache with Redis:

1. Install Redis:
```bash
pip install redis django-redis
```

2. Update `src/settings.py`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Benefits of Redis
- Persistent cache across server restarts
- Shared cache in multi-server setups
- Better performance for high traffic
- More cache storage capacity

## Troubleshooting

### Changes Not Appearing?

1. **Check if plan is active**
   - In admin, verify `is_active` is checked

2. **Clear cache manually**
   ```bash
   python manage.py test_pricing_cache
   ```

3. **Check logs**
   ```bash
   tail -f logs/django.log
   ```
   Look for: "CardPricing ... was updated. Cache invalidated."

4. **Verify signal is registered**
   ```bash
   python manage.py shell
   >>> from checkout.signals import *
   >>> # Should not raise errors
   ```

### Cache Not Working?

1. **Check settings**
   - Verify `CACHES` is configured in `src/settings.py`

2. **Test cache manually**
   ```bash
   python manage.py shell
   >>> from django.core.cache import cache
   >>> cache.set('test', 'value', 60)
   >>> cache.get('test')
   'value'
   ```

### Signals Not Firing?

1. **Check app config**
   - Verify `checkout/apps.py` has `ready()` method
   - Ensure signals are imported

2. **Check installed apps**
   - Verify 'checkout' is in `INSTALLED_APPS`

## Files Modified

1. ✅ `checkout/signals.py` - New file for cache invalidation
2. ✅ `checkout/apps.py` - Updated to register signals
3. ✅ `checkout/views.py` - Added caching to HomeView, CardDetailView, and CheckoutView
4. ✅ `checkout/forms.py` - Made subscription dropdown dynamic ✨ NEW
5. ✅ `checkout/models.py` - Removed hardcoded subscription choices ✨ NEW
6. ✅ `templates/home.html` - Made pricing section dynamic
7. ✅ `templates/checkout/checkout.html` - Made pricing dynamic in JavaScript
8. ✅ `src/settings.py` - Added cache configuration
9. ✅ `checkout/management/commands/test_pricing_cache.py` - Testing utility
10. ✅ `checkout/migrations/0004_alter_checkoutsubmission_subscription_type.py` - New migration ✨ NEW

## Summary

The system now automatically updates all card displays when you change pricing in the admin panel. The cache ensures fast page loads while signals guarantee data freshness. No manual intervention needed!
