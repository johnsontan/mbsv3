from django import forms
from administration.models import Accounts, AccountProfiles, ContactForm
from django.forms import BaseInlineFormSet
from django.forms.utils import ErrorDict
from captcha.fields import ReCaptchaField

class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField()
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5  # Default 5 rows
        })
    )
    class Meta:
        model = ContactForm
        exclude = []

