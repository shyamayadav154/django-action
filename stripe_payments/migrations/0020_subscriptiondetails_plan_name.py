# Generated by Django 3.2 on 2022-07-28 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_payments', '0019_auto_20220729_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptiondetails',
            name='plan_name',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
