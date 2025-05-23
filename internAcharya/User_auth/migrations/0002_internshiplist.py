# Generated by Django 5.1.1 on 2025-04-10 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternshipList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internship_role', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('working_hours', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
