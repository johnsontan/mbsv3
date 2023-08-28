from django.contrib import admin
from .models import CustomerProfile, CreditHistory, Voucher, VoucherHistory

# Register your models here.
admin.site.register(CustomerProfile)
admin.site.register(CreditHistory)
admin.site.register(Voucher)
admin.site.register(VoucherHistory)