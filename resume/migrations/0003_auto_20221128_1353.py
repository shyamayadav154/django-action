# Generated by Django 3.2 on 2022-11-28 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0002_auto_20221128_1250'),
    ]

    operations = [
        
        migrations.AlterField(
            model_name='job_task_suggesstion',
            name='job_title',
            field=models.TextField(blank=True, null=True),
        ),
    ]
