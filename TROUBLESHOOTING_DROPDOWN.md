# Troubleshooting: Empty Subscription Dropdown

## Problem
The subscription type dropdown in `/checkout/` is showing nothing or only "Choose a subscription type..."

## Quick Diagnosis

Run these commands to diagnose:

```bash
# Activate virtual environment
venv\Scripts\activate

# Test 1: Check database
python manage.py shell < debug_pricing.py

# Test 2: Check form
python manage.py shell < test_form_choices.py
```

## Common Causes & Solutions

### Cause 1: No Active Pricing Plans ⭐ MOST COMMON

**Symptoms:**
- Dropdown is empty or only shows placeholder
- Debug script shows "0 active plans"

**Solution:**
```bash
# Option A: Populate default plans
python manage.py populate_pricing

# Option B: Add manually in admin
# 1. Go to http://127.0.0.1:8000/admin/checkout/cardpricing/
# 2. Click "Add Card Pricing"
# 3. Fill in details and CHECK "Is active"
# 4. Save
```

### Cause 2: Migration Not Run

**Symptoms:**
- Error about subscription_type field
- Form doesn't load

**Solution:**
```bash
python manage.py migrate
```

### Cause 3: Server Not Restarted

**Symptoms:**
- Changes not appearing
- Old code still running

**Solution:**
```bash
# Stop server (Ctrl+C)
# Start again
python manage.py runserver
```

### Cause 4: Browser Cache

**Symptoms:**
- Works in incognito mode
- Works after hard refresh

**Solution:**
- Hard refresh: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)
- Or open in incognito/private mode

### Cause 5: JavaScript Error

**Symptoms:**
- Dropdown appears but doesn't work
- Console shows errors

**Solution:**
1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Look for errors related to `subscriptionPricing`

## Step-by-Step Fix

### Step 1: Verify Database Has Plans

```bash
python manage.py shell
```

Then in the shell:
```python
from checkout.models import CardPricing

# Check total plans
print(f"Total plans: {CardPricing.objects.count()}")

# Check active plans
active = CardPricing.objects.filter(is_active=True)
print(f"Active plans: {active.count()}")

# List active plans
for plan in active:
    print(f"  - {plan.name} ({plan.plan_type})")

# Exit
exit()
```

**Expected:** At least 1 active plan

**If 0 plans:** Run `python manage.py populate_pricing`

### Step 2: Verify Form Loads Choices

```bash
python manage.py shell
```

Then:
```python
from checkout.forms import CheckoutForm

form = CheckoutForm()
choices = form.fields['subscription_type'].choices

print(f"Form has {len(choices)} choices:")
for value, label in choices:
    print(f"  {value}: {label}")

exit()
```

**Expected:** Multiple choices (not just empty one)

**If only 1 choice:** Plans exist but form isn't loading them

### Step 3: Clear Cache

```bash
python manage.py test_pricing_cache
```

This clears the cache and shows current data.

### Step 4: Restart Everything

```bash
# Stop server (Ctrl+C)

# Clear cache
python manage.py test_pricing_cache

# Start server
python manage.py runserver
```

### Step 5: Test in Browser

1. Open browser in incognito mode
2. Go to `http://127.0.0.1:8000/checkout/`
3. Check subscription dropdown
4. Open DevTools (F12) and check Console for errors

## Detailed Checks

### Check 1: Model Field

Open `checkout/models.py` and verify:
```python
subscription_type = models.CharField(max_length=100)
# Should NOT have choices= parameter
```

### Check 2: Form Field

Open `checkout/forms.py` and verify:
```python
# At class level
subscription_type = forms.ChoiceField(
    choices=[],
    widget=forms.Select(attrs={'class': 'form-control'}),
    required=True
)

# In __init__ method
subscription_choices = [('', 'Choose a subscription type...')]
subscription_choices.extend([
    (plan.plan_type, plan.name) for plan in pricing_plans
])
self.fields['subscription_type'].choices = subscription_choices
```

### Check 3: View Passes Pricing Map

Open `checkout/views.py` and verify CheckoutView.get():
```python
pricing_map = {plan.plan_type: float(plan.price) for plan in pricing_plans}

return render(request, 'checkout/checkout.html', {
    'form': form,
    'pricing_plans': pricing_plans,
    'pricing_map': pricing_map
})
```

### Check 4: Template Uses Pricing Map

Open `templates/checkout/checkout.html` and verify:
```javascript
const subscriptionPricing = {{ pricing_map|safe }};
```

## Manual Test

Create a test plan manually:

```bash
python manage.py shell
```

```python
from checkout.models import CardPricing

# Create a test plan
plan = CardPricing.objects.create(
    plan_type='test_plan',
    name='Test Plan',
    subtitle='For testing',
    price=1000,
    card_range='1-5',
    features='Test Feature 1\nTest Feature 2',
    is_active=True,
    display_order=99
)

print(f"Created: {plan.name}")

# Verify it exists
active = CardPricing.objects.filter(is_active=True)
print(f"Active plans: {active.count()}")

exit()
```

Now refresh checkout page and check if "Test Plan" appears.

## Still Not Working?

### Check Server Logs

Look for errors in the terminal where Django is running.

### Check Browser Console

1. Open DevTools (F12)
2. Go to Console tab
3. Look for JavaScript errors
4. Look for failed network requests

### Check Form Rendering

View page source and search for:
```html
<select name="subscription_type"
```

Check if it has `<option>` tags inside.

### Enable Debug Mode

In `src/settings.py`:
```python
DEBUG = True
```

This will show detailed error messages.

## Expected Behavior

### In Database
```
CardPricing table has rows with is_active=True
```

### In Form
```python
form.fields['subscription_type'].choices = [
    ('', 'Choose a subscription type...'),
    ('individual', 'Individual Cards'),
    ('sm_business', 'S&M Business'),
    # ... more plans
]
```

### In HTML
```html
<select name="subscription_type" class="form-control">
    <option value="">Choose a subscription type...</option>
    <option value="individual">Individual Cards</option>
    <option value="sm_business">S&M Business</option>
    <!-- ... more options -->
</select>
```

### In JavaScript
```javascript
const subscriptionPricing = {
    "individual": 3900,
    "sm_business": 3600,
    // ... more plans
};
```

## Contact Points

If still stuck, provide:
1. Output of `debug_pricing.py`
2. Output of `test_form_choices.py`
3. Browser console errors (if any)
4. Server terminal errors (if any)

---

**Most Common Fix:** Run `python manage.py populate_pricing` to add default plans!
