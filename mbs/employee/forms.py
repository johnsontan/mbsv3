from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Accounts, AccountProfiles
from PIL import Image
from io import BytesIO
from django.contrib.auth.forms import PasswordChangeForm
from .models import EmployeePayslip, EmployeeLeave, EmployeeLeaveHistory, EmployeeFrontendProfile
from .models import Accounts
from django.utils import timezone
from django.core.exceptions import ValidationError

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
    
    def __init__(self, *args, **kwargs):
        self.employee_leave_profile = kwargs.pop('employee_leave_profile', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        qty = cleaned_data.get('qty')
        leave_type = cleaned_data.get('leave_type')

        # Check if start_date and end_date are provided
        if not start_date:
            self.add_error('start_date', 'Start date is required.')
        if not end_date:
            self.add_error('end_date', 'End date is required.')
        
        #Calculate the total days between start and end date
        total_days = (end_date - start_date).days + 1 #including the start date

        if total_days == 1:
            #quantity can be 0.5 or 1 for single day
            if qty not in [0.5, 1]:
                self.add_error('qty', 'Quantity must be 0.5 or 1 for single day.')
        else:
            #quantity must match the total days or half a day 
            if qty % 1 not in [0.0, 0.5]:
                self.add_error('qty', 'Quantity must be a whole number or end with .5.')
            elif qty != total_days and qty != total_days - 0.5:
                self.add_error('qty', 'Quantity does not match the start & end date.')
            
        # Check leave balance
        if self.employee_leave_profile:
            if leave_type == 'annual leave' and self.employee_leave_profile.annual_leave - qty < 0:
                self.add_error('leave_type', 'Insufficient annual leave')
            elif leave_type == 'childcare leave' and self.employee_leave_profile.childcare_leave - qty < 0:
                self.add_error('leave_type', 'Insufficient childcare leave')
            elif leave_type == 'maternity leave' and self.employee_leave_profile.maternity_leave - qty < 0:
                self.add_error('leave_type', 'Insufficient maternity leave')
            elif leave_type == 'paternity leave' and self.employee_leave_profile.paternity_leave - qty < 0:
                self.add_error('leave_type', 'Insufficient paternity leave')
            elif leave_type == 'sick leave' and self.employee_leave_profile.sick_leave - qty < 0:
                self.add_error('leave_type', 'Insufficient sick leave')
            elif leave_type == 'unpaid leave' and self.employee_leave_profile.unpaid_leave - qty < 0:
                self.add_error('leave_type', 'Insufficient unpaid leave')
        return cleaned_data

class EmployeeFrontendForm(forms.ModelForm):
    class Meta:
        model = EmployeeFrontendProfile
        exclude = []
        