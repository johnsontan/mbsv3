from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission

# Create your models here.


class Accounts(AbstractUser):

    ADMIN = 'admin'
    EMPLOYEE = 'employee'
    Roles = (
        (ADMIN, 'admin'),
        (EMPLOYEE, 'employee')
    )

    email = models.EmailField(primary_key=True, max_length=200, null=False, unique=True)
    role = models.CharField(
        max_length=20,
        choices=Roles,
        default=Roles[1]
    )
    status = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group, related_name="accounts_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="accounts_user_permissions")

    def __str__(self):
        try:
            return self.accountprofile.name
        except AccountProfiles.DoesNotExist:
            return self.email
    
class AccountProfiles(models.Model):
    user = models.OneToOneField(Accounts, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=230)
    address = models.TextField()
    phone_number = models.IntegerField()
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FrontendServices(models.Model):
    id = models.BigAutoField(primary_key=True)
    service_name = models.CharField(max_length=255)
    department = models.CharField(max_length=225)
    sub_department = models.CharField(max_length=225)
    price = models.CharField(max_length=255)

class FrontendBanner(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='frontendbanner/')

class ContactForm(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    message = models.TextField(null=False, blank=False)
    phone_number = models.IntegerField()
    email = models.EmailField(null=False, blank=False)


class Product(models.Model):
    HAIR = 'hair'
    BEAUTY = 'beauty'
    HEALTH = 'health'
    
    Department_choice = (
        (HAIR, 'hair'),
        (BEAUTY, 'beauty'),
        (HEALTH, 'health'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    qty = models.IntegerField(default=0)
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to="productImages/")
    department = models.CharField(choices=Department_choice, max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)