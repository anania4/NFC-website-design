# Generated migration for CardPricing model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardPricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_type', models.CharField(choices=[('individual', 'Individual Cards'), ('sm_business', 'S&M Business'), ('enterprise', 'Enterprise'), ('corporate', 'Corporate')], max_length=20, unique=True)),
                ('name', models.CharField(help_text="Display name (e.g., 'Individual')", max_length=100)),
                ('subtitle', models.CharField(help_text="Short description (e.g., 'Perfect for professionals')", max_length=200)),
                ('price', models.DecimalField(decimal_places=2, help_text='Price in Birr', max_digits=10)),
                ('card_range', models.CharField(help_text="Number of cards (e.g., '1-9 Cards')", max_length=50)),
                ('features', models.TextField(default='Customized Design\n2 Year Subscription\nDigital Profile\nAnalytics Dashboard', help_text="Enter features, one per line (e.g., 'Customized Design')")),
                ('is_featured', models.BooleanField(default=False, help_text="Show 'Best Value' badge")),
                ('is_popular', models.BooleanField(default=False, help_text="Show 'Most Popular' badge")),
                ('display_order', models.IntegerField(default=0, help_text='Order to display (lower numbers first)')),
                ('is_active', models.BooleanField(default=True, help_text='Show this plan on the website')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Card Pricing',
                'verbose_name_plural': 'Card Pricing',
                'ordering': ['display_order', 'plan_type'],
            },
        ),
    ]
