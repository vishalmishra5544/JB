# Generated by Django 2.2.3 on 2023-04-02 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus', '0002_auto_20230402_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='applied_jobs',
            name='status',
            field=models.CharField(default='applied', max_length=20000),
        ),
    ]