# Generated by Django 4.0 on 2021-12-21 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0004_alter_commands_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commands',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
