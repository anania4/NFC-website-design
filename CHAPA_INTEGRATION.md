# Chapa Payment Integration Guide

## Overview

The TAP Digital Business Card checkout system is now fully integrated with Chapa Payment Gateway. When users submit the checkout form, they are redirected to Chapa to complete payment securely.

## How It Works

### User Flow

1. **User fills checkout form** → Personal info, subscription type, uploads
2. **Clicks "Proceed to Payment"** → Form data saved to database
3. **Redirected to Chapa** → Secure payment page opens
4. **Enters payment details** → Credit card, mobile money, etc.
5. **Payment processed** → Chapa handles the transaction
6. **Redirected back** → Returns to success or failure page
7. **Order confirmed** → Admin can see payment status

### Technical Flow

```
┌─────────────────┐
│  Checkout Form  │
│  (User fills)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Submit Form    │
│  POST /checkout/│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Save to DB     │
│  Generate TX_REF│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Call Chapa API │
│  Initialize Pay │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Redirect User  │
│  to Chapa Page  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  User Pays on   │
│  Chapa Platform │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Chapa Callback │
│  /payment/      │
│  callback/      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Verify Payment │
│  Update Status  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Show Success   │
│  or Failure     │
└─────────────────┘
```

## Setup Instructions

### 1. Get Chapa API Keys

1. Go to [https://dashboard.chapa.co](https://dashboard.chapa.co)
2. Sign up or log in
3. Navigate to **Settings → API Keys**
4. Copy your:
   - **Secret Key** (for server-side API calls)
   - **Public Key** (for reference)

### 2. Configure Keys

**Option A: Using .env file (Recommended)**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your keys
CHAPA_SECRET_KEY=CHASECK_TEST-xxxxxxxxxxxxxxxxxx
CHAPA_PUBLIC_KEY=CHAPUBK_TEST-xxxxxxxxxxxxxxxxxx
```

**Option B: Direct in settings.py (Development only)**

Edit `src/settings.py`:

```python
# Chapa Payment Configuration
CHAPA_SECRET_KEY = 'CHASECK_TEST-your-secret-key'
CHAPA_PUBLIC_KEY = 'CHAPUBK_TEST-your-public-key'
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs the `requests` library needed for Chapa API calls.

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the new payment-related fields in the database.

### 5. Test the Integration

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Go to `http://127.0.0.1:8000/checkout/`

3. Fill out the form and click "Proceed to Payment"

4. You should be redirected to Chapa's payment page

5. Use Chapa test cards to complete payment

## Database Fields

### CheckoutSubmission Model

New payment-related fields:

```python
chapa_tx_ref = models.CharField(max_length=100, unique=True)
# Unique transaction reference (auto-generated)
# Format: TAP-XXXXXXXXXXXX

chapa_payment_status = models.CharField(max_length=50, default='pending')
# Status: 'pending', 'success', 'failed'

is_paid = models.BooleanField(default=False)
# True if payment verified and completed
```

## API Endpoints

### 1. Initialize Payment

**Endpoint:** `POST https://api.chapa.co/v1/transaction/initialize`

**Headers:**
```json
{
  "Authorization": "Bearer YOUR_SECRET_KEY",
  "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
  "amount": "3900",
  "currency": "ETB",
  "email": "customer@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "tx_ref": "TAP-ABC123DEF456",
  "callback_url": "https://yoursite.com/payment/callback/",
  "return_url": "https://yoursite.com/payment/callback/",
  "customization": {
    "title": "TAP Digital Business Card",
    "description": "Individual Cards Subscription"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Hosted Link",
  "data": {
    "checkout_url": "https://checkout.chapa.co/checkout/payment/..."
  }
}
```

### 2. Verify Payment

**Endpoint:** `GET https://api.chapa.co/v1/transaction/verify/{tx_ref}`

**Headers:**
```json
{
  "Authorization": "Bearer YOUR_SECRET_KEY"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Payment details",
  "data": {
    "status": "success",
    "amount": 3900,
    "currency": "ETB",
    "tx_ref": "TAP-ABC123DEF456"
  }
}
```

## Admin Dashboard

### Payment Status Display

The admin dashboard now shows:

- **Payment Status Badge**: Color-coded status
  - 🟢 Green: Paid
  - 🟡 Yellow: Pending
  - 🔴 Red: Failed

- **Transaction Reference**: Unique TX_REF for tracking

- **Filter Options**: Filter by payment status

### Viewing Orders

1. Go to `/admin/`
2. Click **Checkout submissions**
3. See payment status for each order
4. Click on an order to see full details including TX_REF

## Testing

### Test Cards (Chapa Sandbox)

Use these test cards in the Chapa test environment:

**Successful Payment:**
- Card Number: `4200 0000 0000 0000`
- CVV: Any 3 digits
- Expiry: Any future date

**Failed Payment:**
- Card Number: `4100 0000 0000 0000`
- CVV: Any 3 digits
- Expiry: Any future date

### Test Flow

1. Fill checkout form with test data
2. Click "Proceed to Payment"
3. Use test card on Chapa page
4. Complete payment
5. Verify redirect back to success page
6. Check admin dashboard for payment status

## URLs

- **Checkout Form**: `/checkout/`
- **Payment Callback**: `/payment/callback/`
- **Success Page**: `/checkout/success/<id>/`

## Troubleshooting

### Payment Not Initializing

**Problem:** User clicks "Proceed to Payment" but nothing happens

**Solutions:**
1. Check if `CHAPA_SECRET_KEY` is set in settings
2. Verify API key is correct
3. Check server logs for API errors
4. Ensure `requests` library is installed

### Callback Not Working

**Problem:** Payment completes but status doesn't update

**Solutions:**
1. Verify callback URL is accessible
2. Check if TX_REF matches
3. Review payment verification logic
4. Check Chapa dashboard for webhook logs

### Amount Mismatch

**Problem:** Wrong amount sent to Chapa

**Solutions:**
1. Verify subscription type pricing in JavaScript
2. Check amount field value before submission
3. Ensure decimal places are correct (2 places)

## Security Notes

1. **Never expose Secret Key**: Keep it in environment variables
2. **Always verify payments**: Don't trust callback alone
3. **Use HTTPS in production**: Required for PCI compliance
4. **Validate amounts**: Check amount matches expected price
5. **Log transactions**: Keep audit trail of all payments

## Production Checklist

- [ ] Replace test API keys with live keys
- [ ] Set `DEBUG = False` in settings
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/SSL
- [ ] Set up proper error logging
- [ ] Configure email notifications
- [ ] Test with real payment methods
- [ ] Set up webhook monitoring
- [ ] Configure backup payment verification

## Support

- **Chapa Documentation**: [https://developer.chapa.co](https://developer.chapa.co)
- **Chapa Support**: support@chapa.co
- **Dashboard**: [https://dashboard.chapa.co](https://dashboard.chapa.co)

## Summary

✅ Chapa payment gateway fully integrated
✅ Secure payment processing
✅ Automatic status updates
✅ Admin dashboard tracking
✅ Test mode ready
✅ Production ready (with live keys)
