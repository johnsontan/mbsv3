# Generated by Django 4.2.4 on 2023-09-13 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_customernotes'),
    ]

    operations = [
        migrations.AddField(
            model_name='credithistory',
            name='entry',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], default='debit', max_length=50),
        ),
        migrations.AddField(
            model_name='packagehistory',
            name='entry',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], default='debit', max_length=50),
        ),
    ]
