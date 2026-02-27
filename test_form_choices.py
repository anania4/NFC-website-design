"""
Test script to verify form choices are loading correctly
Run with: python manage.py shell < test_form_choices.py
"""

print("\n" + "="*60)
print("TESTING CHECKOUT FORM SUBSCRIPTION CHOICES")
print("="*60 + "\n")

# Step 1: Check database
print("Step 1: Checking database for active pricing plans...")
from checkout.models import CardPricing

active_plans = CardPricing.objects.filter(is_active=True).order_by('display_order')
print(f"Found {active_plans.count()} active plans in database:")

if active_plans.count() == 0:
    print("\n❌ NO ACTIVE PLANS FOUND!")
    print("\nYou need to:")
    print("1. Go to: http://127.0.0.1:8000/admin/checkout/cardpricing/")
    print("2. Add pricing plans OR edit existing and check 'Is active'")
    print("3. Save and try again")
    print("\nOR run: python manage.py populate_pricing")
else:
    for plan in active_plans:
        print(f"  ✓ {plan.name} (plan_type: '{plan.plan_type}', price: {plan.price})")

# Step 2: Test form initialization
print("\nStep 2: Testing CheckoutForm initialization...")
try:
    from checkout.forms import CheckoutForm
    
    form = CheckoutForm()
    
    print(f"Form created successfully!")
    print(f"subscription_type field type: {type(form.fields['subscription_type'])}")
    
    choices = form.fields['subscription_type'].choices
    print(f"\nForm has {len(choices)} choices:")
    
    for i, (value, label) in enumerate(choices):
        if value == '':
            print(f"  {i}. (empty) - '{label}'")
        else:
            print(f"  {i}. '{value}' - '{label}'")
    
    if len(choices) <= 1:
        print("\n❌ PROBLEM: Only empty choice exists!")
        print("This means active plans were not loaded into the form.")
    else:
        print(f"\n✓ SUCCESS: Form has {len(choices)-1} subscription options!")
        
except Exception as e:
    print(f"\n❌ ERROR creating form: {e}")
    import traceback
    traceback.print_exc()

# Step 3: Test cache
print("\nStep 3: Checking cache...")
from django.core.cache import cache

cache_key = 'active_pricing_plans'
cached_plans = cache.get(cache_key)

if cached_plans:
    print(f"✓ Cache contains {len(cached_plans)} plans")
else:
    print("ℹ️  Cache is empty (will be populated on first form load)")

print("\n" + "="*60)
print("SUMMARY")
print("="*60 + "\n")

if active_plans.count() == 0:
    print("❌ NO ACTIVE PRICING PLANS")
    print("   Action: Add plans in admin or run populate_pricing command")
elif len(form.fields['subscription_type'].choices) <= 1:
    print("❌ FORM NOT LOADING CHOICES")
    print("   Action: Check for errors above")
else:
    print("✓ EVERYTHING LOOKS GOOD!")
    print(f"  - {active_plans.count()} active plans in database")
    print(f"  - {len(form.fields['subscription_type'].choices)-1} choices in form")
    print("\nIf dropdown still empty in browser:")
    print("  1. Restart Django server")
    print("  2. Hard refresh browser (Ctrl+F5)")
    print("  3. Check browser console for JavaScript errors")

print("\n" + "="*60 + "\n")
