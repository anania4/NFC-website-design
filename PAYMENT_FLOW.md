# Payment Flow - How It Works

## Complete User Journey

### Step 1: User Selects Plan
- User visits homepage pricing section
- Clicks "Get Started" on any plan (Individual, S&M Business, Enterprise, Corporate)
- URL includes subscription parameter: `/checkout/?subscription=enterprise`

### Step 2: Checkout Form
- Form auto-fills subscription type and amount
- User fills in:
  - Personal info (name, title, email)
  - Uploads profile picture and company logo (optional)
  - Adds social media links (optional)
- Clicks "Proceed to Payment" button

### Step 3: Form Submission
**Backend Process:**
```
1. Validate form data
2. Save to database (CheckoutSubmission)
3. Generate unique TX_REF (e.g., TAP-6AF150044C3E)
4. Save social media links
5. Call Chapa API to initialize payment
6. Get checkout URL from Chapa
7. Redirect user to Chapa payment page
```

**Console Output:**
```
📝 Form submitted
✅ Form is valid, creating submission...
✅ Submission created: ID=1, TX_REF=TAP-6AF150044C3E
✅ Social links processed: 1 links
🔄 Initializing Chapa payment...
💰 Amount: 3200 ETB
📡 Chapa API Response Status: 200
✅ Redirecting to: https://checkout.chapa.co/...
```

### Step 4: Chapa Payment Page
- User is redirected to Chapa's secure payment page
- Chapa displays:
  - Merchant: TAP Card
  - Amount: 3200 ETB
  - Description: Enterprise Subscription
- User enters payment details:
  - Credit/Debit card
  - Mobile money
  - Bank transfer

### Step 5: Payment Processing
- Chapa processes the payment
- User sees success or failure message on Chapa
- Chapa redirects back to your site

### Step 6: Return to Your Site
**Callback URL:** `/payment/callback/?tx_ref=TAP-XXX&status=success`

**Backend Process:**
```
1. Receive callback from Chapa
2. Extract tx_ref and status
3. Find order in database
4. Verify payment with Chapa API
5. Update order status:
   - is_paid = True
   - chapa_payment_status = 'success'
6. Redirect to success page
```

### Step 7: Success Page
**URL:** `/checkout/success/1/`

**Displays:**
- 🎉 Success icon
- "Payment Successful!" or "Order Confirmed!"
- Order details:
  - Order ID
  - Customer name
  - Subscription type
  - Amount
  - Payment status (✓ Paid)
  - Transaction ID
  - Order date
- Next steps based on payment status
- Action buttons (Back to Home, Continue Shopping)

## Payment Status Flow

```
┌─────────────┐
│   Pending   │ ← Initial status when order created
└──────┬──────┘
       │
       ├─→ User pays on Chapa
       │
       ▼
┌─────────────┐
│   Success   │ ← Payment verified, is_paid = True
└─────────────┘

       OR

┌─────────────┐
│   Failed    │ ← Payment cancelled/failed
└─────────────┘
```

## Success Page Variations

### If Payment Completed (is_paid = True):
```
🎉 Payment Successful!

Thank you John! Your payment has been processed successfully.
Your TAP card order is confirmed and will be prepared shortly.

Order Details:
- Payment Status: ✓ Paid
- Transaction ID: TAP-6AF150044C3E

What's Next?
✓ Your payment has been confirmed and recorded
✓ Our design team will start preparing your personalized TAP card
✓ You'll receive an email confirmation with order details
✓ Your TAP card will be shipped within 3-5 business days
✓ Track your order status via email updates
```

### If Payment Pending (is_paid = False):
```
🎉 Order Confirmed!

Thank you John! Your TAP card order has been successfully submitted.
We'll be in touch soon to finalize your personalized digital business card.

Order Details:
- Transaction ID: TAP-6AF150044C3E

What's Next?
✓ We'll review your order and contact you within 24 hours
✓ Our design team will prepare your personalized TAP card
✓ You'll receive payment instructions and delivery details
✓ Your TAP card will be shipped once payment is confirmed
```

## URLs Summary

| Page | URL | Purpose |
|------|-----|---------|
| Checkout Form | `/checkout/` | User fills order details |
| Payment Callback | `/payment/callback/` | Chapa returns here after payment |
| Success Page | `/checkout/success/<id>/` | Shows order confirmation |
| Admin Dashboard | `/admin/` | View all orders |

## Testing the Flow

### 1. Test with Chapa Test Cards

**Success Card:**
```
Card Number: 4200 0000 0000 0000
CVV: 123
Expiry: 12/25
```

**Failure Card:**
```
Card Number: 4100 0000 0000 0000
CVV: 123
Expiry: 12/25
```

### 2. Watch Console Logs

Start server and watch for emoji indicators:
```bash
python manage.py runserver
```

### 3. Check Database

After payment, verify in admin:
```
http://127.0.0.1:8000/admin/
→ Checkout submissions
→ See payment status badge (🟢 Paid)
```

## Troubleshooting

### Issue: Not redirecting to Chapa
**Check:**
- Console shows `✅ Redirecting to: https://checkout.chapa.co/...`
- If not, check for API errors in console

### Issue: Callback not working
**Check:**
- URL is accessible: `/payment/callback/`
- TX_REF matches database record
- Chapa can reach your callback URL (use ngrok for local testing)

### Issue: Success page not showing
**Check:**
- URL format: `/checkout/success/1/` (with order ID)
- Order exists in database
- View is properly configured

## Production Checklist

Before going live:
- [ ] Replace test API keys with live keys
- [ ] Set up proper domain for callback URL
- [ ] Configure HTTPS/SSL
- [ ] Test with real payment methods
- [ ] Set up email notifications
- [ ] Configure proper error logging
- [ ] Test callback URL is publicly accessible

## Summary

✅ User fills form → Saved to database
✅ Redirects to Chapa → User pays
✅ Chapa calls back → Payment verified
✅ Success page shown → Order confirmed
✅ Admin can track → Payment status visible

**Everything is working!** 🚀
