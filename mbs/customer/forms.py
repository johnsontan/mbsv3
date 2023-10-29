from PIL import Image
from io import BytesIO
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomerNotes, CustomerProfile, CreditHistory, Package, PackageHistory
from django.utils import timezone
from django import forms
from jsignature.forms import JSignatureField

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        exclude = []

    def clean(self):
        cleaned_data = super().clean()
        
        #Check for negative value
        credit = cleaned_data.get('credit')
        if credit is None:
            credit = 0.0
        if credit < 0:
            self.add_error('credit', 'Credit value cannot be negative')
        
class CustomerNotesForm(forms.ModelForm):
    class Meta:
        model = CustomerNotes
        exclude = []

class CreditHistoryForm(forms.ModelForm):
    class Meta:
        model= CreditHistory
        exclude = []
    
    customer_profile = forms.ModelChoiceField(
        queryset=CustomerProfile.objects.all(),
        label="Customer profile",
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        exclude = []

class PackageHistoryForm(forms.ModelForm):
    class Meta:
        model = PackageHistory
        exclude = []
        signature = JSignatureField()

        