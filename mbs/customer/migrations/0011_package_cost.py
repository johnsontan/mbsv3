# Generated by Django 4.2.4 on 2023-09-18 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_alter_package_balanceqty'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='cost',
            field=models.FloatField(default=0.0),
        ),
    ]