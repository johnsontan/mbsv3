from django.utils import timezone
from django.db import models
from jsignature.fields import JSignatureField

# Create your models here.
class CustomerProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.IntegerField()
    credit = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " / " + str(self.phone_number)

class Package(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    qty = models.IntegerField()
    balanceQty = models.IntegerField(blank=True)
    cost = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    customer_profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="package")

    def __str__(self):
        return self.name

class PackageHistory(models.Model):
    CREDIT = 'credit'
    DEBIT = 'debit'

    Entry_choices = (
        (CREDIT, "Credit"),
        (DEBIT, "Debit")
    )

    id = models.BigAutoField(primary_key=True)
    qty = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    entry = models.CharField(choices=Entry_choices, max_length=50, default=DEBIT)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="packageHistory", blank=True)
    signature = JSignatureField()

    def __str__(self):
        return str(self.package) + " / ID:" + str(self.id) + " / " + str(self.package.customer_profile)

class CreditHistory(models.Model):
    CREDIT = 'credit'
    DEBIT = 'debit'

    Entry_choices = (
        (CREDIT, "Credit"),
        (DEBIT, "Debit")
    )
    id = models.BigAutoField(primary_key=True)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    entry = models.CharField(choices=Entry_choices, max_length=50, default=DEBIT)
    customer_profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="creditHistory", blank=True)
    signature = JSignatureField()

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return str(self.customer_profile) + " / ID:" + str(self.id)

class CustomerNotes(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    customer_profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="customerNotes", blank=True)

    class Meta:
        ordering = ['-created_at']



