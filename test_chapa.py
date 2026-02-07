"""
Quick test script to verify Chapa API connection
Run this with: python test_chapa.py
"""

import requests
import json

# Your Chapa test keys
CHAPA_SECRET_KEY = 'CHASECK_TEST-Xt8KWd58iaw0BaDkAvvKiChEowWz3Fgo'

# Test payment data
payment_data = {
    "amount": "100",
    "currency": "ETB",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "tx_ref": f"TAP-TEST-{int(__import__('time').time())}",
    "callback_url": "http://localhost:8000/payment/callback/",
    "return_url": "http://localhost:8000/payment/callback/",
    "customization": {
        "title": "TAP Digital Business Card",
        "description": "Test Payment"
    }
}

print("🔄 Testing Chapa API connection...")
print(f"📝 TX_REF: {payment_data['tx_ref']}")
print(f"💰 Amount: {payment_data['amount']} ETB")

try:
    response = requests.post(
        "https://api.chapa.co/v1/transaction/initialize",
        json=payment_data,
        headers={
            "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
            "Content-Type": "application/json"
        },
        timeout=10
    )
    
    print(f"\n📡 Response Status: {response.status_code}")
    print(f"📄 Response Body:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            print(f"\n✅ SUCCESS!")
            print(f"🔗 Checkout URL: {data.get('data', {}).get('checkout_url')}")
        else:
            print(f"\n❌ API returned non-success status")
    else:
        print(f"\n❌ API request failed")
        
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
