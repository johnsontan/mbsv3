# Generated by Django 4.2.4 on 2023-10-08 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0005_contactform_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactform',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
