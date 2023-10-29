# Generated by Django 4.2.4 on 2023-10-23 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0003_delete_serviceimages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleservices',
            name='department',
            field=models.CharField(choices=[('hair', 'hair'), ('beauty', 'beauty'), ('health', 'health'), ('hair product', 'hair product'), ('beauty product', 'beauty product')], max_length=200),
        ),
        migrations.AlterField(
            model_name='salestransaction',
            name='payment_type',
            field=models.CharField(choices=[('cash', 'cash'), ('paynow', 'paynow'), ('creditcard', 'credit card'), ('nets', 'nets'), ('grab', 'grab'), ('package', 'package'), ('credit sales', 'credit sales'), ('refund', 'refund')], max_length=200),
        ),
    ]
