# Generated by Django 3.2.11 on 2023-01-17 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0007_alter_employee_rfid_tag_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='rfid_tag_number',
            field=models.IntegerField(blank=True, default=None, null=True, unique=True),
        ),
    ]
