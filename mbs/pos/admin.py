from django.contrib import admin
from .models import SaleServices, SalesTransaction

# Register your models here.
admin.site.register(SaleServices)
admin.site.register(SalesTransaction)
