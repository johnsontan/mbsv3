from django import forms
from django.forms import inlineformset_factory
from .models import SalesTransaction, SaleServices
from administration.models import Accounts, AccountProfiles
from django.forms import BaseInlineFormSet
from django.forms.utils import ErrorDict
import math


class CustomSaleServiceFormset(BaseInlineFormSet):
    def get_total_service_price(self):
        """Calculate the total service price from all forms."""
        total = 0
        for form in self.forms:
            # Ensure the form is valid and not marked for deletion before including its price
            if form.is_valid() and not form.cleaned_data.get('DELETE'):
                total += form.cleaned_data.get('service_price', 0)
        return total

class SaleServiceForm(forms.ModelForm):
    class Meta:
        model = SaleServices
        fields = ['id', 'department', 'service_name', 'service_price']

    def __init__(self, *args, **kwargs):
        super(SaleServiceForm, self).__init__(*args, **kwargs)
        # Set the initial value of service_price to None
        self.fields['service_price'].initial = None

    def is_empty(self):
        """Check if the form is effectively empty."""
        for field in self.fields:
            if self.cleaned_data.get(field):
                return False
        return True

    def clean(self):
        if self.cleaned_data.get('DELETE'):
            # If the form is marked for deletion, bypass other validations
            # This assumes DELETE is a valid field in the form
            return self.cleaned_data
        if self.is_empty():
            # If the form is effectively empty but not marked for deletion, raise an error
            raise forms.ValidationError("Empty form. Either fill in or mark for deletion.")
        return super().clean()



class SalesTransactionForm(forms.ModelForm):
    class Meta:
        model = SalesTransaction
        fields = ['grand_total', 'payment_type', 'personal_remarks', 'customer_remarks', 'customer', 'user', 'package_history', 'credit_history']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = Accounts.objects.filter(role='employee')

    def clean(self):
        # Get the cleaned data from the base clean method
        cleaned_data = super().clean()
        grand_total = cleaned_data.get('grand_total')

        # Check if the formset has been passed to this form's instance
        if hasattr(self, 'formset'):
            total_service_price = self.formset.get_total_service_price()
            grand_total = math.ceil(grand_total)
            total_service_price = math.ceil(total_service_price)
            # Validate that the grand total equals the total service price
            if grand_total != total_service_price:
                msg = f"Grand total must be equal to the total service price. Expected {total_service_price}, but got {grand_total}."
                self.add_error('grand_total', msg)
        
        check_user = cleaned_data.get('user')
        if not check_user:
            self.add_error('user', 'Employee is required.')

        return cleaned_data

SaleServiceFormset = inlineformset_factory(
    SalesTransaction, 
    SaleServices, 
    form=SaleServiceForm,
    formset=CustomSaleServiceFormset,  # use your custom formset here
    fields=('id', 'department', 'service_name', 'service_price'), 
    extra=1,
    can_delete=True, # this is important to allow deletion
    can_delete_extra=True
)

class SelectDatesForm(forms.Form):
    startDate = forms.DateField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    endDate = forms.DateField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    employee = forms.ModelChoiceField(queryset=Accounts.objects.filter(role=Accounts.EMPLOYEE), required=False)

    widgets = {
            'startDate': forms.DateTimeInput(attrs={'type': 'date'}),
            'endDate': forms.DateTimeInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        startDate = cleaned_data.get('startDate')
        endDate = cleaned_data.get('endDate')

        if startDate and endDate:
            if startDate > endDate:
                raise forms.ValidationError({
                    'endDate': ['End date cannot be before start date.']
                })
        return cleaned_data
    
class SendEmailReceiptForm(forms.Form):
    email_address = forms.EmailField(required=True)
    receipt_pk = forms.IntegerField(required=True)