# Generated by Django 4.2.4 on 2023-09-01 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeePayslip',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('payment_type', models.CharField(choices=[('cash', 'cash'), ('giro', 'giro'), ('banktrf', 'bank trf')], max_length=200)),
                ('salary_total', models.FloatField(blank=True, default=0.0, null=True)),
                ('basic_total', models.FloatField(blank=True, default=0.0, null=True)),
                ('overtime_total', models.FloatField(blank=True, default=0.0, null=True)),
                ('commission_total', models.FloatField(blank=True, default=0.0, null=True)),
                ('deduction_total', models.FloatField(blank=True, default=0.0, null=True)),
                ('period_start_date', models.DateTimeField()),
                ('period_end_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
