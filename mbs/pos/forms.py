from django import forms
from django.forms import inlineformset_factory
from .models import SalesTransaction, SaleServices, ServiceImages
from administration.models import Accounts, AccountProfiles

class SalesTransactionForm(forms.ModelForm):
    class Meta:
        model = SalesTransaction
        fields = ['grand_total', 'payment_type', 'personal_remarks', 'customer_remarks', 'customer', 'user', 'package_history', 'credit_history']

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = Accounts.objects.filter(role='employee')


# Create inline formsets
SaleServiceFormset = inlineformset_factory(
    SalesTransaction, SaleServices, fields=('department', 'service_name', 'service_price'), extra=1
)

ServiceImageFormset = inlineformset_factory(
    SaleServices, ServiceImages, fields=('image',), extra=1
)