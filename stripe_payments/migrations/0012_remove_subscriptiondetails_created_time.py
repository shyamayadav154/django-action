# Generated by Django 3.2 on 2022-07-18 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_payments', '0011_auto_20220718_1505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptiondetails',
            name='created_time',
        ),
    ]
