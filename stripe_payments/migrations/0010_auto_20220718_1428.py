# Generated by Django 3.2 on 2022-07-18 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_payments', '0009_auto_20220714_0351'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptiondetails',
            name='created_time',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='subscriptiondetails',
            name='updated_time',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
