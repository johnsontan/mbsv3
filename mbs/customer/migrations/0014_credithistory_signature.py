# Generated by Django 4.2.4 on 2023-10-23 11:49

from django.db import migrations
import jsignature.fields


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0013_alter_package_balanceqty_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='credithistory',
            name='signature',
            field=jsignature.fields.JSignatureField(default=''),
        ),
    ]
