"""
Debug script to check pricing data
Run with: python manage.py shell < debug_pricing.py
"""

print("\n" + "="*60)
print("PRICING DEBUG INFORMATION")
print("="*60 + "\n")

# Check if CardPricing table exists and has data
from checkout.models import CardPricing

print("1. Checking CardPricing table...")
try:
    all_plans = CardPricing.objects.all()
    print(f"   Total plans in database: {all_plans.count()}")
    
    if all_plans.count() > 0:
        print("\n   All plans:")
        for plan in all_plans:
            print(f"   - {plan.name} ({plan.plan_type})")
            print(f"     Price: {plan.price} Birr")
            print(f"     Active: {plan.is_active}")
            print(f"     Display Order: {plan.display_order}")
            print()
    else:
        print("   ⚠️  NO PLANS FOUND IN DATABASE!")
        print("   You need to add pricing plans in the admin panel.")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n2. Checking ACTIVE plans only...")
try:
    active_plans = CardPricing.objects.filter(is_active=True).order_by('display_order')
    print(f"   Active plans: {active_plans.count()}")
    
    if active_plans.count() > 0:
        print("\n   Active plans that should appear:")
        for plan in active_plans:
            print(f"   - {plan.name} ({plan.plan_type}) - {plan.price} Birr")
    else:
        print("   ⚠️  NO ACTIVE PLANS!")
        print("   Go to admin and make sure at least one plan has 'is_active' checked.")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n3. Checking cache...")
try:
    from django.core.cache import cache
    
    cache_key = 'active_pricing_plans'
    cached_plans = cache.get(cache_key)
    
    if cached_plans:
        print(f"   ✓ Cache exists with {len(cached_plans)} plans")
        for plan in cached_plans:
            print(f"   - {plan.name} ({plan.plan_type})")
    else:
        print("   ℹ️  Cache is empty (this is OK on first load)")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n4. Testing form choices...")
try:
    from checkout.forms import CheckoutForm
    
    form = CheckoutForm()
    choices = form.fields['subscription_type'].choices
    
    print(f"   Form has {len(choices)} choices:")
    for value, label in choices:
        if value:
            print(f"   - Value: '{value}', Label: '{label}'")
        else:
            print(f"   - (Empty choice: '{label}')")
            
    if len(choices) <= 1:
        print("\n   ⚠️  PROBLEM: Form only has empty choice!")
        print("   This means no active plans were loaded.")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("RECOMMENDATIONS")
print("="*60 + "\n")

try:
    active_count = CardPricing.objects.filter(is_active=True).count()
    
    if active_count == 0:
        print("❌ NO ACTIVE PLANS FOUND")
        print("\nTo fix:")
        print("1. Go to: http://127.0.0.1:8000/admin/checkout/cardpricing/")
        print("2. Either:")
        print("   a) Add new pricing plans, OR")
        print("   b) Edit existing plans and check 'Is active'")
        print("3. Save")
        print("4. Refresh checkout page")
    else:
        print(f"✓ You have {active_count} active plan(s)")
        print("\nIf dropdown still empty:")
        print("1. Clear cache: python manage.py test_pricing_cache")
        print("2. Restart server")
        print("3. Hard refresh browser (Ctrl+F5)")
        
except Exception as e:
    print(f"Error checking plans: {e}")

print("\n" + "="*60 + "\n")
