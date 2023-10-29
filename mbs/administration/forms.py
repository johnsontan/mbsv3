from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Accounts, AccountProfiles, Product, ProductHistory, FrontendBanner
from PIL import Image
from io import BytesIO
from django.contrib.auth.forms import PasswordChangeForm

class EmailUserCreationForm(UserCreationForm):
    class Meta:
        model = Accounts
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].min_length = 8

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # set the email as the username as well
        if commit:
            user.save()
        return user

class AccountProfileForm(forms.ModelForm):
    class Meta:
        model = AccountProfiles
        fields = ['name', 'address', 'phone_number', 'dob', 'image']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
        
        def clean_image(self):
            image = self.cleaned_data.get('image')
            if(image):
                if image.content_type not in ['image/jpeg', 'image/png']:
                    raise forms.ValidationError("Only JPEG and PNG images are allowed.")
                
                img = Image.open(image)

                #Reduce image quality (Compression)
                output = BytesIO()
                img.save(output, format='JPEG', quality=60)

                self.cleaned_date['image'] = output
            return image

class AccountForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = ['email', 'password']

class AccountEmailForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = ['email', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].validators = []

    def clean_email(self):
        cleaned_data = super().clean()
        email = self.cleaned_data.get('email')
        
        if email == self.instance.email:
            return email  # Email hasn't changed, no need to check for duplicates
        
        if Accounts.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Email address is already in use.")
        
        return email

class OptionalPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].required = False
        self.fields['new_password1'].required = False
        self.fields['new_password2'].required = False

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        old_password = self.cleaned_data.get('old_password')

        if not new_password1 and not old_password:
            return None

        return super().clean_new_password2()
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []
    
    description = forms.CharField(widget=forms.Textarea)

class ProductHistoryForm(forms.ModelForm):
    class Meta:
        model = ProductHistory
        exclude = []
        
class FrontEndBannerForm(forms.ModelForm):
    class Meta:
        model = FrontendBanner
        exclude = []