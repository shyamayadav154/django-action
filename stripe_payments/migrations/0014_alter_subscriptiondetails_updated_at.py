# Generated by Django 3.2 on 2022-07-18 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_payments', '0013_rename_updated_time_subscriptiondetails_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptiondetails',
            name='updated_at',
            field=models.DateField(),
        ),
    ]
