# Generated by Django 3.2.9 on 2021-12-07 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
        ('attendance', '0002_alter_attendancelog_emp_out_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancelog',
            name='emp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee', to_field='emp_id'),
        ),
    ]
