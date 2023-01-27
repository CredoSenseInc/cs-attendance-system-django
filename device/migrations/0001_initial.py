# Generated by Django 3.2.11 on 2023-01-27 13:12

import device.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='deviceInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(default='EMPTY', max_length=255)),
                ('device_id', models.CharField(default=device.models.generate_unique_id, max_length=15, unique=True)),
                ('device_deptartment', models.CharField(blank=True, max_length=255, null=True)),
                ('device_location', models.CharField(blank=True, max_length=255, null=True)),
                ('device_emp_count', models.IntegerField(blank=True, default=0, null=True)),
                ('firmware_version', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='firmware',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(default='0.0.1', max_length=255)),
                ('url', models.CharField(default='http://credosense.com/downloads', max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('changelog', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='commands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isExecuted', models.BooleanField(default=False)),
                ('message', models.CharField(max_length=255)),
                ('server_message', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('scan_time', models.DateTimeField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.deviceinfo', to_field='device_id')),
            ],
        ),
    ]
