# Generated by Django 3.2 on 2022-12-07 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_tracking', '0002_tracking_job_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracking',
            name='shortcode_url',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
