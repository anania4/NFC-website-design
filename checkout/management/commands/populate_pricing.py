from django.core.management.base import BaseCommand
from checkout.models import CardPricing


class Command(BaseCommand):
    help = 'Populate initial card pricing data'

    def handle(self, *args, **options):
        pricing_data = [
            {
                'plan_type': 'individual',
                'name': 'Individual',
                'subtitle': 'Perfect for professionals',
                'price': 3900,
                'card_range': '1-9 Cards',
                'features': 'Customized Design\n2 Year Subscription\nDigital Profile\nAnalytics Dashboard',
                'is_popular': True,
                'is_featured': False,
                'display_order': 1,
            },
            {
                'plan_type': 'sm_business',
                'name': 'S&M Business',
                'subtitle': 'For small & medium teams',
                'price': 3600,
                'card_range': '10-24 Cards',
                'features': 'Customized Design\n2 Year Subscription\nDigital Profile\nTeam Analytics',
                'is_popular': False,
                'is_featured': False,
                'display_order': 2,
            },
            {
                'plan_type': 'enterprise',
                'name': 'Enterprise',
                'subtitle': 'For growing companies',
                'price': 3200,
                'card_range': '25-49 Cards',
                'features': 'Customized Design\n2 Year Subscription\nDigital Profile\nPriority Support',
                'is_popular': False,
                'is_featured': False,
                'display_order': 3,
            },
            {
                'plan_type': 'corporate',
                'name': 'Corporate',
                'subtitle': 'For large organizations',
                'price': 2500,
                'card_range': '50+ Cards',
                'features': 'Customized Design\n2 Year Subscription\nAdmin Panel\nDedicated Support',
                'is_popular': False,
                'is_featured': True,
                'display_order': 4,
            },
        ]

        created_count = 0
        updated_count = 0

        for data in pricing_data:
            plan, created = CardPricing.objects.update_or_create(
                plan_type=data['plan_type'],
                defaults=data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created pricing plan: {plan.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated pricing plan: {plan.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created: {created_count}, Updated: {updated_count}'
            )
        )
