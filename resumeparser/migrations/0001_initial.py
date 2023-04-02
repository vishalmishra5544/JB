# Generated by Django 2.2.3 on 2023-04-02 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(upload_to='resumes/', verbose_name='Upload Resumes')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('mobile_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='Mobile Number')),
                ('education', models.CharField(blank=True, max_length=255, null=True, verbose_name='Education')),
                ('skills', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Skills')),
                ('designation', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Designation')),
                ('experience', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Experience')),
                ('uploaded_on', models.DateTimeField(auto_now_add=True, verbose_name='Uploaded On')),
            ],
        ),
    ]
