# Generated by Django 4.2.4 on 2023-09-28 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleservices',
            name='sales_transaction',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pos.salestransaction'),
        ),
        migrations.AlterField(
            model_name='serviceimages',
            name='sale_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pos.saleservices'),
        ),
    ]
