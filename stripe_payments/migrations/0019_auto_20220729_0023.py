# Generated by Django 3.2 on 2022-07-28 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_payments', '0018_auto_20220718_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptiondetails',
            name='amount',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='subscriptiondetails',
            name='invoice_pdf',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
