from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
from datetime import datetime
from django.forms import ValidationError
from django.core.exceptions import ValidationError
from pillow_heif import register_heif_opener, HeifFile
from PIL import Image
import io


def validate_image_size(image):
    # Validate file size (30MB max)
    filesize = image.size
    if filesize > 30 * 1024 * 1024:  # 30MB limit
        raise ValidationError("The maximum file size allowed is 30MB.")

    try:
        # Read file into memory as BytesIO
        image_file = io.BytesIO(image.read())
        image.seek(0)  # Rewind file pointer

        # Attempt to open the image
        try:
            img = Image.open(image_file)

            # Handle MPO (Multi-Picture Object) by forcing the first frame
            if img.format == 'MPO':  # Misinterpreted as MPO
                img.seek(0)  # Force first frame
                img = img.convert('RGB')  # Convert to RGB explicitly
                format = 'JPEG'  # Treat it as JPEG
            else:
                format = img.format  # Get image format detected by Pillow

        except UnidentifiedImageError:
            raise ValidationError('Invalid image. Could not identify format.')

        # Supported formats
        valid_image_formats = ['JPEG', 'PNG']
        if format.upper() not in valid_image_formats:
            raise ValidationError('Invalid image format. Supported formats: JPEG, PNG.')

    except Exception as e:
        raise ValidationError(f'Invalid image. Error: {str(e)}')
    
    
# Create your models here.

class Accounts(AbstractUser):

    ADMIN = 'admin'
    EMPLOYEE = 'employee'
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    Roles = (
        (ADMIN, 'admin'),
        (EMPLOYEE, 'employee')
    )
    Status_choice = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive')
    )

    email = models.EmailField(max_length=200, null=False, unique=True)
    username = models.CharField(max_length=150, unique=False, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=Roles,
        default=EMPLOYEE
    )
    status = models.CharField(null=False, blank=False, max_length=150, choices=Status_choice, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group, related_name="accounts_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="accounts_user_permissions")


    def __str__(self):
        if hasattr(self, 'accountprofile'):
            return self.accountprofile.name
        return self.email
    

class AccountProfiles(models.Model):
    user = models.OneToOneField(Accounts, on_delete=models.CASCADE, related_name="accountprofile")
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=230)
    address = models.TextField(null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='accountProfileImages/', null=True, blank=True, default="anonymous-display-pic.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FrontendBanner(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='frontendbanner/')
    selected = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ContactForm(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    message = models.TextField(null=False, blank=False)
    phone_number = models.IntegerField()
    email = models.EmailField(null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    HAIR = 'hair'
    BEAUTY = 'beauty'
    HEALTH = 'health'
    
    Department_choice = (
        (HAIR, 'hair'),
        (BEAUTY, 'beauty'),
        (HEALTH, 'health'),
    )
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    qty = models.IntegerField()
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    product_image = models.FileField(upload_to='products/', null=True, validators=[validate_image_size]) 
    department = models.CharField(choices=Department_choice, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

class ProductHistory(models.Model):
    ADD = 'add'
    SUBSTRACT = 'substract'

    Entry_choices = (
        (ADD, 'add'),
        (SUBSTRACT, 'substract')
    )

    id = models.BigAutoField(primary_key=True)
    editQty = models.IntegerField(blank=True, null=True)
    entry = models.CharField(max_length=60, choices=Entry_choices, blank=True)
    notes = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productHistory", null=True, blank=True)
    name = models.ForeignKey(AccountProfiles, on_delete=models.DO_NOTHING, related_name="productHistoryName", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class YoutubeVideos(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    thumbnail_url = models.CharField(max_length=255)
    video_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)