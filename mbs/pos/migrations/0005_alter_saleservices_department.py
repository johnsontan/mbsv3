# Generated by Django 4.2.4 on 2023-12-22 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0004_alter_saleservices_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleservices',
            name='department',
            field=models.CharField(choices=[('hair', 'hair'), ('beauty', 'beauty'), ('health', 'health'), ('hair product', 'hair product'), ('beauty product', 'beauty product'), ('package sales', 'package sales'), ('credit sales', 'credit sales')], max_length=200),
        ),
    ]