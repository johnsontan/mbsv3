from django.db import models
from jsignature.fields import JSignatureField

# Create your models here.
class CustomerProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.IntegerField(max_length=16)
    credit = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

class Voucher(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    qty = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    customer_profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)

class VoucherHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    qty = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    signature = JSignatureField()

class CreditHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    customer_profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)

