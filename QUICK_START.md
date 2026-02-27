# Quick Start Guide - Real-Time Card Updates

## 🚀 Get Started in 5 Minutes

### Step 1: Activate Virtual Environment (30 seconds)

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 2: Start Server (10 seconds)

```bash
python manage.py runserver
```

### Step 3: Test the System (2 minutes)

#### Open Admin Panel
```
http://127.0.0.1:8000/admin/
```

Login with your admin credentials.

#### Update a Price
1. Click **Checkout** → **Card Pricing**
2. Click on any plan (e.g., "Individual")
3. Change the price (e.g., 3900 → 4000)
4. Click **Save**

#### Verify Update
Open in new tabs:
- Homepage: `http://127.0.0.1:8000/`
- Card Detail: `http://127.0.0.1:8000/card-detail/`
- Checkout: `http://127.0.0.1:8000/checkout/`

**You should see the new price on all pages!** 🎉

### Step 4: Test Cache System (30 seconds)

```bash
python manage.py test_pricing_cache
```

Expected output:
```
=== Testing Pricing Cache ===

✓ Cache exists with 4 plans
  - Individual: 4000.0 Birr
  - S&M Business: 3600.0 Birr
  - Enterprise: 3200.0 Birr
  - Corporate: 2500.0 Birr

✓ Database has 4 active plans
  ...

Clearing cache...
✓ Cache cleared successfully

=== Test Complete ===
```

## ✅ That's It!

Your real-time card update system is working!

## 📖 What Next?

### For Admins
Read: `ADMIN_PRICING_QUICK_GUIDE.md`

### For Developers
Read: `CARD_STATUS_UPDATE_GUIDE.md`

### For Deployment
Read: `DEPLOYMENT_CHECKLIST.md`

### For Complete Overview
Read: `UPDATE_SUMMARY.md`

## 🎯 Key Features

✅ Update pricing in admin panel
✅ Changes appear instantly on website
✅ No cache clearing needed
✅ No server restart needed
✅ Fast page loads (cached)
✅ Automatic synchronization

## 💡 Quick Tips

### Update Price
1. Admin → Card Pricing
2. Edit plan
3. Save
4. Done!

### Hide a Plan
1. Admin → Card Pricing
2. Edit plan
3. Uncheck "Is active"
4. Save

### Reorder Plans
1. Admin → Card Pricing
2. Change "Display order" (1, 2, 3, 4)
3. Save

### Add Badge
1. Admin → Card Pricing
2. Check "Is popular" or "Is featured"
3. Save

## 🆘 Need Help?

### Changes not showing?
```bash
# Clear cache
python manage.py test_pricing_cache

# Hard refresh browser
Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
```

### Server won't start?
```bash
# Check for errors
python manage.py check
```

### Cache not working?
```bash
# Test cache
python manage.py shell
>>> from django.core.cache import cache
>>> cache.set('test', 'value', 60)
>>> cache.get('test')
```

## 📚 Full Documentation

All documentation is in the project root:

| File | Purpose |
|------|---------|
| `QUICK_START.md` | This file - get started fast |
| `ADMIN_PRICING_QUICK_GUIDE.md` | Admin quick reference |
| `CARD_STATUS_UPDATE_GUIDE.md` | Technical guide |
| `DEPLOYMENT_CHECKLIST.md` | Deployment steps |
| `UPDATE_SUMMARY.md` | Summary of changes |
| `BEFORE_AFTER_COMPARISON.md` | Before/after comparison |
| `SYSTEM_ARCHITECTURE.md` | System overview |
| `FINAL_CHECKLIST.md` | Complete checklist |

---

**Ready to go!** 🚀

Start by updating a price in the admin panel and watch it appear instantly on your website.
