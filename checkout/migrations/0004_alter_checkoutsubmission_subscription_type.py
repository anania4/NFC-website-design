# Generated migration to make subscription_type dynamic

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_alter_cardpricing_plan_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutsubmission',
            name='subscription_type',
            field=models.CharField(max_length=100),
        ),
    ]
