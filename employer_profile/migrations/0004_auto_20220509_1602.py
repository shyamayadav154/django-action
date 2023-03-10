# Generated by Django 3.2 on 2022-05-09 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer_profile', '0003_employer_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer_template',
            name='Experience',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='employer_template',
            name='Job_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='employer_template',
            name='Location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='employer_template',
            name='Notice_time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='employer_template',
            name='Salary_offered',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='employer_template',
            name='Subskills',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
