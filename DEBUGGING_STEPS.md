# Debugging Steps for Chapa Integration

## Step 1: Test Chapa API Connection

Run this command to test if Chapa API is working:

```bash
python test_chapa.py
```

**Expected Output:**
- ✅ SUCCESS! with a checkout URL
- If you see errors, check your internet connection or API keys

## Step 2: Check Django Server Logs

1. Start the Django server:
```bash
python manage.py runserver
```

2. Open your browser to: `http://127.0.0.1:8000/checkout/`

3. Fill out the form and click "Proceed to Payment"

4. **Watch the terminal/console** for these messages:
   - `📝 Form submitted`
   - `✅ Form is valid, creating submission...`
   - `✅ Submission created: ID=X, TX_REF=...`
   - `🔄 Initializing Chapa payment...`
   - `✅ Redirecting to: https://checkout.chapa.co/...`

## Step 3: Common Issues & Solutions

### Issue 1: Form Not Submitting
**Symptoms:** Nothing happens when clicking "Proceed to Payment"

**Check:**
1. Open browser console (F12) and look for JavaScript errors
2. Check if button is clickable
3. Verify CSRF token is present in form

**Solution:**
- Clear browser cache
- Try in incognito/private mode
- Check browser console for errors

### Issue 2: Form Validation Errors
**Symptoms:** Page reloads but stays on checkout

**Check Terminal for:**
- `❌ Form errors: {...}`

**Solution:**
- Fill all required fields
- Check email format
- Ensure amount is a valid number
- Check file upload sizes (max 5MB)

### Issue 3: Chapa API Not Configured
**Symptoms:** See warning message about API keys

**Check Terminal for:**
- `⚠️ WARNING: CHAPA_SECRET_KEY not configured properly`

**Solution:**
- Verify `src/settings.py` has correct Chapa keys
- Keys should start with `CHASECK_TEST-` or `CHASECK-`

### Issue 4: Chapa API Error
**Symptoms:** Error message about payment initialization

**Check Terminal for:**
- `❌ Chapa API Error: ...`
- `🌐 Network error connecting to Chapa`

**Solution:**
- Check internet connection
- Verify API keys are correct
- Try test script: `python test_chapa.py`
- Check Chapa dashboard for API status

### Issue 5: Database Migration Error
**Symptoms:** Can't save submission

**Solution:**
```bash
# Delete the problematic migration
rm checkout/migrations/0002_*.py

# Create fresh migrations
python manage.py makemigrations checkout

# Apply migrations
python manage.py migrate
```

## Step 4: Enable Test Mode

If Chapa is not configured, the system will automatically:
1. Save the order to database
2. Skip payment
3. Redirect to success page
4. Show warning message

This allows you to test the form without Chapa.

## Step 5: Check Browser Network Tab

1. Open browser DevTools (F12)
2. Go to "Network" tab
3. Submit the form
4. Look for POST request to `/checkout/`
5. Check response:
   - Status 302 = Redirect (good!)
   - Status 200 = Form error (check response)
   - Status 500 = Server error (check terminal)

## Step 6: Verify Database

Check if submission was created:

```bash
python manage.py shell
```

Then run:
```python
from checkout.models import CheckoutSubmission
submissions = CheckoutSubmission.objects.all()
print(f"Total submissions: {submissions.count()}")
for s in submissions:
    print(f"ID: {s.id}, Name: {s.first_name} {s.last_name}, Status: {s.chapa_payment_status}")
```

## Quick Fix: Reset Everything

If nothing works, try this:

```bash
# 1. Stop the server (Ctrl+C)

# 2. Delete database
del db.sqlite3

# 3. Delete migrations
del checkout\migrations\0002_*.py

# 4. Recreate database
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Start server
python manage.py runserver
```

## Need Help?

If you're still stuck, provide:
1. Terminal output when submitting form
2. Browser console errors (F12)
3. Output from `python test_chapa.py`
