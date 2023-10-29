from django.db import models
from administration.models import Accounts, AccountProfiles
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class EmployeePayslip(models.Model):
    CASH = 'cash'
    GIRO = 'giro'
    BANK_TRF = 'banktrf'

    Payment_choice = (
        (CASH, 'cash'),
        (GIRO, 'giro'),
        (BANK_TRF, 'bank trf')
    )
    id = models.BigAutoField(primary_key=True)
    payment_type = models.CharField(choices=Payment_choice, max_length=200)
    salary_total = models.FloatField(null=True, blank=True, default=0.0)
    basic_total = models.FloatField(null=True, blank=True, default=0.0)
    overtime_total = models.FloatField(null=True, blank=True, default=0.0)
    commission_total = models.FloatField(null=True, blank=True, default=0.0)
    deduction_total = models.FloatField(null=True, blank=True, default=0.0)
    period_start_date = models.DateTimeField(null=False, blank=False)
    period_end_date = models.DateTimeField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Accounts, on_delete=models.DO_NOTHING)

class EmployeeLeave(models.Model):

    id = models.BigAutoField(primary_key=True)
    annual_leave = models.FloatField(default=0.0)
    childcare_leave = models.FloatField(default=0.0)
    maternity_leave = models.FloatField(default=0.0)
    paternity_leave = models.FloatField(default=0.0)
    sick_leave = models.FloatField(default=0.0)
    unpaid_leave = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(Accounts, on_delete=models.CASCADE, related_name='employeeLeave')

    def __str__(self):
        return str(self.user)

class EmployeeLeaveHistory(models.Model):

    ANNUAL_LEAVE = 'annual leave'
    CHILDCARE_LEAVE = 'childcare leave'
    MATERNITY_LEAVE = 'maternity leave'
    PATERNITY_LEAVE = 'paternity leave'
    SICK_LEAVE = 'sick leave'
    UNPAID_LEAVE = 'unpaid leave'

    ADD = 'add'
    SUBSTRACT = 'substract'

    APPROVED = 'approved'
    REJECTED = 'rejected'
    PENDING = 'pending'

    Leave_choices = (
        (ANNUAL_LEAVE, 'annual leave'),
        (CHILDCARE_LEAVE, 'childcare leave'),
        (MATERNITY_LEAVE, 'maternity leave'),
        (PATERNITY_LEAVE, 'paternity leave'),
        (SICK_LEAVE, 'sick leave'),
        (UNPAID_LEAVE, 'unpaid leave')
    )

    Entry_choices = (
        (ADD, 'add'),
        (SUBSTRACT, 'substract')
    )

    Status_choices = (
        (APPROVED, 'approved'),
        (REJECTED, 'rejected'),
        (PENDING, 'pending')
    )

    id = models.BigAutoField(primary_key=True)
    notes = models.TextField(blank=True, null=True)
    leave_type = models.CharField(max_length=200, choices=Leave_choices)
    entry = models.CharField(max_length=150, choices=Entry_choices, blank=True)
    picture = models.ImageField(upload_to="employeeLeaveHistory/", blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    qty = models.FloatField(default=0.0)
    status = models.CharField(max_length=88, choices=Status_choices, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    employeeLeave = models.ForeignKey(EmployeeLeave, on_delete=models.CASCADE, related_name="employeeLeaveHistroy", blank=True)

class EmployeeFrontendProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    employee_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="employeeFrontendProfile/")
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=Accounts)
def create_employee_leave(sender, instance, created, **kwargs):
    if created:
        EmployeeLeave.objects.create(user=instance)

# Connect the signal handler function to the post_save signal of the Accounts model
post_save.connect(create_employee_leave, sender=Accounts)
