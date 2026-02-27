# Deployment Checklist - Real-Time Card Updates

## Pre-Deployment Steps

### 1. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Verify Django Installation
```bash
python manage.py check
```

Expected output: `System check identified no issues (0 silenced).`

### 3. Run Migrations (if needed)
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Test Cache System
```bash
python manage.py test_pricing_cache
```

Expected output:
```
=== Testing Pricing Cache ===

✓ Cache exists with X plans
  - Individual: 3900.0 Birr
  - S&M Business: 3600.0 Birr
  ...

✓ Database has X active plans
  ...

Clearing cache...
✓ Cache cleared successfully

=== Test Complete ===
```

### 5. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

## Deployment Steps

### 1. Backup Database
```bash
# SQLite backup
copy db.sqlite3 db.sqlite3.backup

# Or use Django command
python manage.py dumpdata > backup.json
```

### 2. Deploy Code
```bash
# Pull latest code
git pull origin main

# Or copy files manually
```

### 3. Restart Server

**Development**:
```bash
python manage.py runserver
```

**Production (Passenger)**:
```bash
touch tmp/restart.txt
```

**Production (Gunicorn)**:
```bash
sudo systemctl restart gunicorn
```

**Production (uWSGI)**:
```bash
sudo systemctl restart uwsgi
```

### 4. Verify Deployment

Visit these URLs and verify:
- [ ] Homepage: `/` - Pricing section shows dynamic data
- [ ] Card Detail: `/card-detail/` - All plans display correctly
- [ ] Admin Panel: `/admin/checkout/cardpricing/` - Can edit plans

### 5. Test Real-Time Updates

1. Go to admin panel
2. Edit any pricing plan
3. Change the price
4. Save
5. Refresh homepage in another tab
6. Verify new price appears

## Post-Deployment Verification

### Check Logs
```bash
# View recent logs
tail -f logs/django.log

# Search for cache events
cat logs/django.log | grep "CardPricing"
```

Expected log entries:
```
INFO CardPricing 'Individual' was updated. Cache invalidated.
```

### Monitor Performance

Check these metrics:
- [ ] Page load time (should be faster)
- [ ] Database queries (should be reduced)
- [ ] Cache hit rate (should be high)

### Test All Features

- [ ] Update price → Appears on website
- [ ] Toggle is_active → Plan shows/hides
- [ ] Change display_order → Cards reorder
- [ ] Update features → Changes appear
- [ ] Toggle badges → Badges show/hide
- [ ] Create new plan → Appears on website
- [ ] Delete plan → Disappears from website

## Rollback Plan

If issues occur:

### 1. Restore Database
```bash
# SQLite restore
copy db.sqlite3.backup db.sqlite3

# Or use Django command
python manage.py loaddata backup.json
```

### 2. Revert Code
```bash
git revert HEAD
# Or restore previous version
```

### 3. Clear Cache
```bash
python manage.py test_pricing_cache
```

### 4. Restart Server
```bash
touch tmp/restart.txt
# Or appropriate restart command
```

## Production Configuration

### Recommended: Upgrade to Redis

1. **Install Redis**:
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# CentOS/RHEL
sudo yum install redis

# macOS
brew install redis
```

2. **Install Python Redis Client**:
```bash
pip install redis django-redis
```

3. **Update settings.py**:
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

4. **Start Redis**:
```bash
# Ubuntu/Debian
sudo systemctl start redis-server
sudo systemctl enable redis-server

# macOS
brew services start redis
```

5. **Test Redis Connection**:
```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.set('test', 'value', 60)
>>> cache.get('test')
'value'
```

## Monitoring Setup

### 1. Set Up Log Rotation

Create `/etc/logrotate.d/django-tap`:
```
/path/to/project/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        touch /path/to/project/tmp/restart.txt
    endscript
}
```

### 2. Monitor Cache Performance

Add to cron:
```bash
# Check cache status every hour
0 * * * * /path/to/venv/bin/python /path/to/project/manage.py test_pricing_cache >> /path/to/logs/cache_monitor.log 2>&1
```

### 3. Set Up Alerts

Monitor for:
- High error rate in logs
- Cache connection failures
- Slow page load times
- Database connection issues

## Security Checklist

- [ ] DEBUG = False in production
- [ ] SECRET_KEY is secure and not in version control
- [ ] ALLOWED_HOSTS is properly configured
- [ ] HTTPS is enabled
- [ ] Admin panel uses strong passwords
- [ ] Database backups are automated
- [ ] Logs are secured and rotated

## Performance Optimization

### 1. Enable Compression
Already configured with WhiteNoise:
```python
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

### 2. Database Optimization
```bash
# SQLite optimization
python manage.py dbshell
PRAGMA optimize;
VACUUM;
.quit
```

### 3. Cache Warming
Add to startup script:
```python
# In management command or startup
from django.core.cache import cache
from checkout.models import CardPricing

pricing_plans = list(CardPricing.objects.filter(is_active=True).order_by('display_order'))
cache.set('active_pricing_plans', pricing_plans, 3600)
```

## Troubleshooting

### Issue: Server won't start
```bash
# Check for syntax errors
python manage.py check

# Check for migration issues
python manage.py showmigrations

# Check logs
tail -f logs/django.log
```

### Issue: Cache not working
```bash
# Test cache manually
python manage.py shell
>>> from django.core.cache import cache
>>> cache.set('test', 'value', 60)
>>> cache.get('test')
```

### Issue: Changes not appearing
```bash
# Clear cache
python manage.py test_pricing_cache

# Check if plan is active
python manage.py shell
>>> from checkout.models import CardPricing
>>> CardPricing.objects.filter(is_active=True).count()
```

## Support Contacts

- **Technical Issues**: Check `CARD_STATUS_UPDATE_GUIDE.md`
- **Admin Questions**: Check `ADMIN_PRICING_QUICK_GUIDE.md`
- **Quick Reference**: Check `ADMIN_QUICK_REFERENCE.md`

## Success Criteria

Deployment is successful when:
- ✅ All pages load without errors
- ✅ Pricing displays correctly on homepage
- ✅ Pricing displays correctly on card detail page
- ✅ Admin can update pricing
- ✅ Changes appear immediately on website
- ✅ Cache system is working
- ✅ Logs show cache invalidation events
- ✅ No performance degradation

---

**Last Updated**: February 27, 2026
**Status**: Ready for Deployment
