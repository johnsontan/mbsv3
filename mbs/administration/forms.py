from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Accounts, AccountProfiles, Product, ProductHistory, FrontendBanner
from PIL import Image
from io import BytesIO
from django.contrib.auth.forms import PasswordChangeForm
from django.core.files.base import ContentFile
import pillow_heif

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

        # Check if a new image has been uploaded
        if 'product_image' in self.changed_data:
            image = Image.open(instance.product_image)

            # Handle HEIC images by converting to JPEG
            if image.format.lower() == 'heic':
                heif_file = pillow_heif.read_heif(instance.product_image)
                image = Image.frombytes(
                    heif_file.mode,
                    heif_file.size,
                    heif_file.data,
                    "raw",
                    heif_file.mode,
                    heif_file.stride,
                )
                format = 'JPEG'
            elif image.format.lower() in ['jpeg', 'jpg']:
                format = 'JPEG'
            elif image.format.lower() == 'png':
                format = 'PNG'
            else:
                raise ValueError(f"Unsupported image format: {image.format}")

            # Resize values
            target_height = 500
            aspect_ratio = image.width / image.height
            target_width = int(target_height * aspect_ratio)

            # Resize the image
            image = image.resize((target_width, target_height), Image.ANTIALIAS)

            # Save the image back to the model
            temp_image = BytesIO()
            image.save(temp_image, format=format)
            temp_image.seek(0)

            instance.product_image.save(instance.product_image.name, ContentFile(temp_image.read()), save=False)
            temp_image.close()

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