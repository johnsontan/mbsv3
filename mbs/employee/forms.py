from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Accounts, AccountProfiles
from PIL import Image
from io import BytesIO
from django.contrib.auth.forms import PasswordChangeForm
from .models import EmployeePayslip, EmployeeLeave, EmployeeLeaveHistory, EmployeeFrontendProfile
from .models import Accounts
from django.utils import timezone

class employeePayslipForm(forms.ModelForm):
    class Meta:
        model = EmployeePayslip
        exclude = []
        widgets = {
            'period_start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'period_end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #query active employees
        active_employees = Accounts.objects.filter(status=Accounts.ACTIVE, role=Accounts.EMPLOYEE)
        self.fields['user'].queryset = active_employees

    def clean(self):
        cleaned_data = super().clean()
        period_start_date = cleaned_data.get('period_start_date')
        period_end_date = cleaned_data.get('period_end_date')

        #check if vars is valid 
        if period_start_date and period_end_date:
            current_datetime = timezone.now()
            print("period_start_date:", period_start_date)
            print("period_end_date:", period_end_date)
            print("current_datetime:", current_datetime)

            if period_start_date > current_datetime:
                self.add_error('period_start_date', 'Start date cannot be in the future.')
            if period_end_date > current_datetime:
                self.add_error('period_end_date', 'End date cannot be in the future.')
            if period_start_date > period_end_date:
                self.add_error('period_end_date', 'End date cannot be earlier than start date.')
        
        #salary === basic_total + overtime_total + commission_total - deduction_total
        salary = cleaned_data.get('salary_total')
        basic = cleaned_data.get('basic_total')
        overtime = cleaned_data.get('overtime_total')
        commission = cleaned_data.get('commission_total')
        deduction = cleaned_data.get('deduction_total')
        if salary < 0:
            self.add_error('salary_total', 'Salary must be greater than zero')
        if salary != (basic + overtime + commission - deduction):
            self.add_error('salary_total', 'Salary must be equal to (basic + overtime + commission - deduction)')


class EmployeeLeaveHistoryForm(forms.ModelForm):
    class Meta:
        model = EmployeeLeaveHistory
        exclude = []
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'date'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

class EmployeeFrontendForm(forms.ModelForm):
    class Meta:
        model = EmployeeFrontendProfile
        exclude = []
        