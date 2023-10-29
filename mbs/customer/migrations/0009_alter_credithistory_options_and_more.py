# Generated by Django 4.2.4 on 2023-09-18 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_alter_credithistory_customer_profile_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='credithistory',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='customernotes',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='package',
            name='balanceQty',
            field=models.IntegerField(default=0),
        ),
    ]
