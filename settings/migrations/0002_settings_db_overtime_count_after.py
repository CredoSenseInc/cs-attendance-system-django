# Generated by Django 3.2.11 on 2022-01-12 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings_db',
            name='overtime_count_after',
            field=models.TimeField(default='17:20:00'),
        ),
    ]
