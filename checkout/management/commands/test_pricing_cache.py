"""
Management command to test pricing cache invalidation
"""
from django.core.management.base import BaseCommand
from django.core.cache import cache
from checkout.models import CardPricing


class Command(BaseCommand):
    help = 'Test pricing cache invalidation'

    def handle(self, *args, **options):
        cache_key = 'active_pricing_plans'
        
        self.stdout.write(self.style.WARNING('\n=== Testing Pricing Cache ===\n'))
        
        # Check current cache
        cached_data = cache.get(cache_key)
        if cached_data:
            self.stdout.write(self.style.SUCCESS(f'✓ Cache exists with {len(cached_data)} plans'))
            for plan in cached_data:
                self.stdout.write(f'  - {plan.name}: {plan.price} Birr')
        else:
            self.stdout.write(self.style.WARNING('✗ Cache is empty'))
        
        # Show database data
        db_plans = CardPricing.objects.filter(is_active=True).order_by('display_order')
        self.stdout.write(self.style.SUCCESS(f'\n✓ Database has {db_plans.count()} active plans'))
        for plan in db_plans:
            self.stdout.write(f'  - {plan.name}: {plan.price} Birr (Active: {plan.is_active})')
        
        # Clear cache
        self.stdout.write(self.style.WARNING('\nClearing cache...'))
        cache.delete(cache_key)
        
        cached_data = cache.get(cache_key)
        if cached_data is None:
            self.stdout.write(self.style.SUCCESS('✓ Cache cleared successfully'))
        else:
            self.stdout.write(self.style.ERROR('✗ Failed to clear cache'))
        
        self.stdout.write(self.style.SUCCESS('\n=== Test Complete ===\n'))
