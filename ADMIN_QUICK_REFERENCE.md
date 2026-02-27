# Admin Panel Quick Reference

## 🎯 NEW: Real-Time Card Updates

**Great news!** When you update card pricing in the admin panel, changes now appear **instantly** on the website. No cache clearing or server restart needed!

### How It Works
1. Edit any card pricing
2. Click Save
3. Website updates automatically
4. Cache refreshes in the background

See [CARD_STATUS_UPDATE_GUIDE.md](CARD_STATUS_UPDATE_GUIDE.md) for technical details.

---

## Managing Card Pricing

### Quick Steps to Update Pricing

1. Go to: `http://127.0.0.1:8000/admin/`
2. Login with admin credentials
3. Click "Card Pricing" under "CHECKOUT"
4. Click on the plan you want to edit
5. Make your changes
6. Click "Save"
7. Changes appear immediately on the website

### Common Tasks

#### Change a Price
1. Edit the plan
2. Update the "Price" field (e.g., 3900.00)
3. Save

#### Add/Remove Features
1. Edit the plan
2. Go to "Features" field
3. Add or remove lines (one feature per line)
4. Save

Example:
```
Customized Design
2 Year Subscription
Digital Profile
Analytics Dashboard
Priority Support
```

#### Change Badge
- **Most Popular**: Check "Is popular"
- **Best Value**: Check "Is featured"
- **No Badge**: Uncheck both

#### Reorder Plans
1. Edit each plan
2. Set "Display order" (1, 2, 3, 4)
3. Lower numbers appear first (left to right)
4. Save

#### Hide a Plan
1. Edit the plan
2. Uncheck "Is active"
3. Save
4. Plan disappears from website but stays in database

#### Show a Hidden Plan
1. Edit the plan
2. Check "Is active"
3. Save

### Field Reference

| Field | Description | Example |
|-------|-------------|---------|
| Plan type | Unique identifier | individual, sm_business, enterprise, corporate |
| Name | Display title | "Individual" |
| Subtitle | Short description | "Perfect for professionals" |
| Price | Price in Birr | 3900.00 |
| Card range | Number of cards | "1-9 Cards" |
| Features | One per line | See example above |
| Is featured | "Best Value" badge | ☑ or ☐ |
| Is popular | "Most Popular" badge | ☑ or ☐ |
| Display order | Position (1-4) | 1 = leftmost |
| Is active | Show on website | ☑ = visible |

## Managing Orders

### View All Orders
1. Click "Checkout submissions" under "CHECKOUT"
2. See list of all orders with payment status

### Search Orders
- Use search box at top
- Search by: name, email, transaction reference

### Filter Orders
- By subscription type
- By payment status
- By date

### View Order Details
1. Click on any order
2. See all information including:
   - Customer details
   - Uploaded images
   - Social media links
   - Payment status

### Payment Status Colors
- 🟢 Green "✓ Paid" = Successfully paid
- 🟡 Yellow "⏳ Pending" = Payment pending
- 🔴 Red "✗ Failed" = Payment failed

## Maintenance Commands

### Test Cache System (NEW!)

Test that pricing updates are working correctly:

```bash
python manage.py test_pricing_cache
```

This shows:
- Current cached pricing data
- Database pricing data
- Cache clearing confirmation

### Clean Up Old Pending Orders

Run periodically to remove old unpaid orders:

```bash
# Clean orders older than 24 hours (default)
python manage.py cleanup_pending_orders

# Clean orders older than 6 hours
python manage.py cleanup_pending_orders --hours 6
```

### Reset Pricing to Defaults

If you need to restore default pricing:

```bash
python manage.py populate_pricing
```

This updates existing plans without creating duplicates.

## Tips

✅ **DO:**
- Test price changes during low-traffic times
- Keep feature lists consistent across plans
- Use clear, concise descriptions
- Set appropriate display order for logical flow
- Mark your most popular plan with a badge

❌ **DON'T:**
- Delete plans unless absolutely necessary (hide them instead)
- Use special characters in features that might break formatting
- Set multiple plans with the same display order
- Forget to save after making changes

## Troubleshooting

### Changes Not Showing
1. Hard refresh browser (Ctrl+F5 or Cmd+Shift+R)
2. Clear browser cache
3. Check "Is active" is checked
4. Verify server is running

### Can't Login to Admin
```bash
# Create new superuser
python manage.py createsuperuser
```

### Database Issues
```bash
# Run migrations
python manage.py migrate
```

## Support

For technical issues, refer to:
- [PRICING_SETUP.md](PRICING_SETUP.md) - Detailed pricing setup guide
- [README.md](README.md) - Full project documentation

For urgent issues, contact the development team.
