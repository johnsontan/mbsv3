from django.contrib import admin
from .models import CustomerProfile, CreditHistory, Package, PackageHistory

# Register your models here.
admin.site.register(CustomerProfile)
admin.site.register(CreditHistory)
admin.site.register(Package)
admin.site.register(PackageHistory)