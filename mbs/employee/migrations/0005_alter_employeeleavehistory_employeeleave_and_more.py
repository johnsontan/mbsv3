# Generated by Django 4.2.4 on 2023-09-28 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_alter_employeeleavehistory_employeeleave_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeleavehistory',
            name='employeeLeave',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='employeeLeaveHistroy', to='employee.employeeleave'),
        ),
        migrations.AlterField(
            model_name='employeeleavehistory',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
