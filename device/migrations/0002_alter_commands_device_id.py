# Generated by Django 3.2.9 on 2021-12-07 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commands',
            name='device_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.deviceinfo', to_field='device_id'),
        ),
    ]
