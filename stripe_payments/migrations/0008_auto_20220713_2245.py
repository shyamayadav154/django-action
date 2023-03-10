# Generated by Django 3.2 on 2022-07-13 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_payments', '0007_plandetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptiondetails',
            name='payment',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='subscriptiondetails',
            name='customer_id',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='subscriptiondetails',
            name='payment_gateway',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='subscriptiondetails',
            name='status',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='subscriptiondetails',
            name='subscription_id',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
