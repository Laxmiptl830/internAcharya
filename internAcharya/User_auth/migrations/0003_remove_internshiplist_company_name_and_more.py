# Generated by Django 5.1.1 on 2025-04-10 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_auth', '0002_internshiplist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internshiplist',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='internshiplist',
            name='internship_role',
        ),
        migrations.RemoveField(
            model_name='internshiplist',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='internshiplist',
            name='working_hours',
        ),
        migrations.AddField(
            model_name='internshiplist',
            name='company',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='internshiplist',
            name='logo',
            field=models.ImageField(default='company_logos/default.png', upload_to='company_logos/'),
        ),
        migrations.AddField(
            model_name='internshiplist',
            name='role',
            field=models.CharField(default='Software Intern', max_length=100),
        ),
        migrations.AddField(
            model_name='internshiplist',
            name='work_hours',
            field=models.CharField(choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time')], default='Full-time', max_length=20),
        ),
        migrations.AlterField(
            model_name='internshiplist',
            name='location',
            field=models.CharField(default='Remote', max_length=100),
        ),
    ]
