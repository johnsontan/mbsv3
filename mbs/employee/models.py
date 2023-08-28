from django.db import models
from administration.models import Accounts

# Create your models here.

class EmployeePayslip(models.Model):
    CASH = 'cash'
    GIRO = 'giro'
    BANK_TRF = 'banktrf'

    Payment_choice = (
        (CASH, 'cash'),
        (GIRO, 'giro'),
        (BANK_TRF, 'bank trf')
    )
    id = models.BigAutoField(primary_key=True)
    payment_type = models.CharField(choices=Payment_choice, max_length=200)
    salary_total = models.FloatField(null=True, blank=True, default=0.0)
    basic_total = models.FloatField(null=True, blank=True, default=0.0)
    overtime_total = models.FloatField(null=True, blank=True, default=0.0)
    commission_total = models.FloatField(null=True, blank=True, default=0.0)
    deduction_total = models.FloatField(null=True, blank=True, default=0.0)
    period_start_date = models.DateTimeField(null=False, blank=False)
    period_end_date = models.DateTimeField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Accounts, on_delete=models.DO_NOTHING)
