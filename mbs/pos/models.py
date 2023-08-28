from django.db import models
from administration.models import Accounts
from customer.models import CustomerProfile, VoucherHistory, CreditHistory

# Create your models here.

class SalesTransaction(models.Model):
    CASH = 'cash'
    PAYNOW = 'paynow'
    CREDIT_CARD = 'creditcard'
    NETS = 'nets'
    GRAB = 'grab'
    PACKAGE = 'package'
    IN_STORE_CREDIT = 'instorecredit'
    REFUND = 'refund'

    Payment_Choice = (
        (CASH, 'cash'),
        (PAYNOW, 'paynow'),
        (CREDIT_CARD, 'credit card'),
        (NETS, 'nets'),
        (GRAB, 'grab'),
        (PACKAGE, 'package'),
        (IN_STORE_CREDIT, "in store credit"),
        (REFUND, 'refund')
    )

    id = models.BigAutoField(primary_key=True)
    grand_total = models.FloatField(default=0.0)
    payment_type = models.CharField(choices=Payment_Choice, max_length=200)
    personal_remarks = models.TextField()
    customer_remarks = models.TextField()
    customer = models.ForeignKey(CustomerProfile ,on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Accounts, on_delete=models.DO_NOTHING)
    voucher_history = models.ForeignKey(VoucherHistory, on_delete=models.DO_NOTHING, null=True, blank=True)
    credit_history = models.ForeignKey(CreditHistory, on_delete=models.DO_NOTHING, null=True, blank=True)

class SaleServices(models.Model):
    HAIR = 'hair'
    BEAUTY = 'beauty'
    HEALTH = 'health'

    Department_choice = (
        (HAIR, 'hair'),
        (BEAUTY, 'beauty'),
        (HEALTH, 'health')
    )
    id = models.BigAutoField(primary_key=True)
    department = models.CharField(choices=Department_choice, max_length=200)
    service_name = models.CharField(max_length=220)
    service_price = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

class ServiceImages(models.Model):
    sale_service = models.ForeignKey(SaleServices, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='serviceimages/')

