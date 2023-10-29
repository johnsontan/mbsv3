from django import forms
from administration.models import Accounts, AccountProfiles, ContactForm
from django.forms import BaseInlineFormSet
from django.forms.utils import ErrorDict
from captcha.fields import ReCaptchaField

class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = ContactForm
        exclude = []

