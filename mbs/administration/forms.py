from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import Accounts, AccountProfiles, Product, ProductHistory, FrontendBanner
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from django.contrib.auth.forms import PasswordChangeForm
from django.core.files.base import ContentFile
import logging
from PIL import Image
from django.core.files.base import ContentFile
import io
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)

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
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)

        # Process the image only if it was uploaded or changed
        if 'product_image' in self.changed_data and instance.product_image:
            try:
                # Reject unsupported formats early (MPO)
                if instance.product_image.name.lower().endswith('.mpo'):
                    raise ValueError("MPO format is not supported.")

                # Read image into memory
                image_bytes = instance.product_image.read()
                image_file = io.BytesIO(image_bytes)
                image_file.seek(0)  # Reset pointer

                # Attempt to open the image
                try:
                    img = Image.open(image_file)
                    format = img.format
                except UnidentifiedImageError:
                    raise ValueError("Invalid image format.")

                # Validate supported formats
                supported_formats = ['JPEG', 'PNG']
                if format.upper() not in supported_formats:
                    raise ValueError(f"Unsupported image format: {format}")

                # Resize and compress
                max_size = 2000  # Max dimensions (width/height)
                quality = 70     # Compression quality (%)

                if img.height > max_size or img.width > max_size:
                    aspect_ratio = img.width / img.height
                    if img.width > img.height:
                        new_width = max_size
                        new_height = int(max_size / aspect_ratio)
                    else:
                        new_height = max_size
                        new_width = int(max_size * aspect_ratio)
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)

                # Save compressed image
                temp_image = io.BytesIO()
                img.save(temp_image, format=format, quality=quality)
                temp_image.seek(0)

                # Update model image
                instance.product_image.save(
                    instance.product_image.name.split('.')[0] + f'.{format.lower()}',
                    ContentFile(temp_image.read()),
                    save=False
                )
                temp_image.close()

            except Exception as e:
                logger.error(f"Failed to process image: {str(e)}")
                raise ValueError(f"Failed to process image: {str(e)}")

        instance.save()
        return instance


class ProductHistoryForm(forms.ModelForm):
    class Meta:
        model = ProductHistory
        exclude = []
        
class FrontEndBannerForm(forms.ModelForm):
    class Meta:
        model = FrontendBanner
        exclude = []

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        label=_("Email Address")
    )