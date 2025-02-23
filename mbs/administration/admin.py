from django.contrib import admin
from .models import Accounts, AccountProfiles, FrontendBanner, ContactForm, Product

# Register your models here.
admin.site.register(Accounts)
admin.site.register(AccountProfiles)
admin.site.register(FrontendBanner)
admin.site.register(ContactForm)
admin.site.register(Product)