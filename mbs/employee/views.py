from django.shortcuts import render, redirect, get_object_or_404
from administration.decorator import employee_role_required, admin_role_required
from administration.forms import AccountEmailForm, OptionalPasswordChangeForm, AccountProfileForm
from django.contrib import messages
from administration.models import Accounts, AccountProfiles
from django.core.paginator import Paginator
from .forms import employeePayslipForm, EmployeeLeaveHistoryForm, EmployeeFrontendForm
from .models import EmployeePayslip, EmployeeLeave, EmployeeLeaveHistory, EmployeeFrontendProfile
from django.core.paginator import Paginator
from PIL import Image
from django.core.files.base import ContentFile
import io
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

@employee_role_required
def employeeIndex(request):
    return render(request, 'employee-index.html')

@employee_role_required
def employeeProfile(request):
    if request.method == 'POST':
        accountForm = AccountEmailForm(data=request.POST, instance=request.user, initial={'email': request.user.email})
        passwordForm = OptionalPasswordChangeForm(request.user, request.POST)
        profileForm = AccountProfileForm(request.POST, request.FILES, instance=request.user.accountprofile)
        if profileForm.is_valid():
            profile_instance = profileForm.save(commit=False)
            profile_instance.user = request.user  # Set the user instance
            profile_instance.save()
        if accountForm.is_valid():
            accountForm.save()
        else:
            print("Account Form Errors:", accountForm.errors)
        if passwordForm.is_valid():
            #Using custom password change implements django form hence have to verify & save the password manually 
            #The custom password change form only make the passwords optional 
            old_password = passwordForm.cleaned_data.get('old_password')
            new_password1 = passwordForm.cleaned_data.get('new_password1')
            new_password2 = passwordForm.cleaned_data.get('new_password2')

            if old_password and request.user.check_password(old_password):
                if new_password1 == new_password2:
                    request.user.set_password(new_password1)
                    request.user.save()
                    messages.success(request, 'Profile updated')
                    return redirect("employeeIndex")
                else:
                    passwordForm.add_error('new_password2', "Passwords do not match.")
            else:
                passwordForm.add_error('old_password', "Your old password was entered incorrectly. Please enter it again.")
        else:
            print("Password Form Errors:", passwordForm.errors)
        messages.success(request, 'Profile updated')
        return redirect("employeeIndex")
    else:
        #extract user and Account form 
        user = request.user
        accountForm = AccountEmailForm(instance=user)
        passwordForm = OptionalPasswordChangeForm(request.user)
        #Get user account profile instant & pre-fill the form 
        profile_instance = user.accountprofile
        profileForm = AccountProfileForm(instance=profile_instance)
        return render(request, 'employee-profile.html', {"user":user, "profileForm":profileForm, "accountForm":accountForm, "passwordForm":passwordForm})
    
@admin_role_required
def adminEmployeeOverview(request):
    allEmployees = Accounts.objects.filter(role=Accounts.EMPLOYEE)
    return render(request, 'admin-employee-overview.html', {'page':allEmployees})

@admin_role_required
def adminEmployeeEditProfile(request, id):
    try:
        employee = AccountProfiles.objects.get(id=id)
    except AccountProfiles.DoesNotExist:
        employee = None

    if employee == None:
        return redirect('adminEmployeeOverview')
    else:
        if request.method == 'POST':
            accountForm = AccountEmailForm(data=request.POST, instance=employee.user, initial={'email': employee.user.email})
            profileForm = AccountProfileForm(request.POST, request.FILES, instance=employee)
            if profileForm.is_valid():
                profile_instance = profileForm.save(commit=False)
                profile_instance.user = employee.user  # Set the user instance
                profile_instance.save()
            if accountForm.is_valid():
                accountForm.save()
            else:
                print("Account Form Errors:", accountForm.errors)
            messages.success(request, 'Profile updated')
            return redirect("adminEmployeeOverview")
        else:
            #extract user and Account form 
            accountForm = AccountEmailForm(instance=employee.user)
            #Get user account profile instant & pre-fill the form 
            profile_instance = employee
            profileForm = AccountProfileForm(instance=profile_instance)
            return render(request, 'admin-employee-edit.html', {"user":employee, "profileForm":profileForm, "accountForm":accountForm})

@admin_role_required
def adminEmployeePayslipOverview(request):
    payslips = EmployeePayslip.objects.all().order_by("-created_at")

    return render(request, 'admin-employee-payslip-overview.html', {"page":payslips})

@admin_role_required
def adminInsertEmployeePayslip(request):
    if request.method == 'POST':
        form = employeePayslipForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'employee payslip created')
            return redirect('adminInsertEmployeePayslip')
        else:
            print(form.errors)
    else:
        form = employeePayslipForm

    return render(request, 'admin-employee-payslip.html', {"form":form})

@admin_role_required
def adminEditemployeePayslip(request, payslipID):
    payslip = get_object_or_404(EmployeePayslip, pk=payslipID)
    if request.method == 'POST':
        form = employeePayslipForm(request.POST, instance=payslip)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payslip updated')
            return redirect('adminEmployeePayslipOverview')
    else:
        form = employeePayslipForm(instance=payslip)
    return render(request, 'admin-employee-payslip.html', {"form":form})

@admin_role_required
def adminDeleteEmployeePayslip(request, payslipID):
    #Get payslip or 404
    payslip = EmployeePayslip.objects.get(id=payslipID)

    if payslip is not None:
        payslip.delete()
        messages.success(request, 'Payslip deleted')
        return redirect('adminEmployeePayslipOverview') 
    else:
        messages.success(request, 'Error in deleting payslip')
        return redirect('adminEmployeePayslipOverview') 
    

@employee_role_required
def employeePayslipOverview(request):
    #fetch payslip
    payslips = EmployeePayslip.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'employee-payslip-overview.html', {'page':payslips})

@employee_role_required
def employeePayslipViewMore(request, id):
    payslip = EmployeePayslip.objects.filter(id=id).get()
    if request.user != payslip.user:
        return redirect('logout')
    return render(request, 'employee-payslip-view-more.html', {"payslip":payslip})

@admin_role_required
def adminEmployeeLeaveOverview(request):
    employeesLeave = EmployeeLeave.objects.all()
    pendingRequest = EmployeeLeaveHistory.objects.all()
    return render(request, 'admin-employee-leave-overview.html', {"employeesLeave":employeesLeave, "pendingRequest":pendingRequest})

@admin_role_required
def adminEmployeeLeaveInsert(request):
    if request.method == 'POST':
        form = EmployeeLeaveHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            formInstance = form.save(commit=False)
            print(formInstance.picture)
            formInstance.status = EmployeeLeaveHistory.APPROVED
            employeeLeaveProfile = EmployeeLeave.objects.filter(id=formInstance.employeeLeave.id).get()
            if formInstance.entry == 'add':
                if formInstance.leave_type == 'annual leave':
                    employeeLeaveProfile.annual_leave += formInstance.qty
                    employeeLeaveProfile.save()
                elif formInstance.leave_type == 'childcare leave':
                    employeeLeaveProfile.childcare_leave += formInstance.qty
                    employeeLeaveProfile.save()
                elif formInstance.leave_type == 'maternity leave':
                    employeeLeaveProfile.maternity_leave += formInstance.qty
                    employeeLeaveProfile.save()
                elif formInstance.leave_type == 'paternity leave':
                    employeeLeaveProfile.paternity_leave += formInstance.qty
                    employeeLeaveProfile.save()
                elif formInstance.leave_type == 'sick leave':
                    employeeLeaveProfile.sick_leave += formInstance.qty
                    employeeLeaveProfile.save()
                elif formInstance.leave_type == 'unpaid leave':
                    employeeLeaveProfile.unpaid_leave += formInstance.qty
                    employeeLeaveProfile.save()
            else:
                if formInstance.leave_type == 'annual leave' and not employeeLeaveProfile.annual_leave - formInstance.qty < 0:
                    employeeLeaveProfile.annual_leave -= formInstance.qty
                    employeeLeaveProfile.save()
                elif formInstance.leave_type == 'childcare leave' and not employeeLeaveProfile.childcare_leave - formInstance.qty < 0:
                    employeeLeaveProfile.childcare_leave -= formInstance.qty
                    employeeLeaveProfile.save()
                elif formInstance.leave_type == 'maternity leave' and not employeeLeaveProfile.maternity_leave - formInstance.qty < 0:
                    employeeLeaveProfile.maternity_leave -= formInstance.qty
                    employeeLeaveProfile.save()
                elif formInstance.leave_type == 'paternity leave' and not employeeLeaveProfile.paternity_leave - formInstance.qty < 0:
                    employeeLeaveProfile.paternity_leave -= formInstance.qty
                    employeeLeaveProfile.save()
                elif formInstance.leave_type == 'sick leave' and not employeeLeaveProfile.sick_leave - formInstance.qty < 0:
                    employeeLeaveProfile.sick_leave -= formInstance.qty
                    employeeLeaveProfile.save()
                elif formInstance.leave_type == 'unpaid leave' and not employeeLeaveProfile.unpaid_leave - formInstance.qty < 0:
                    employeeLeaveProfile.unpaid_leave -= formInstance.qty
                    employeeLeaveProfile.save()
                else:
                    form.add_error('qty', 'Insufficient quantity')

            if form.errors:  # Check if there are any errors in the form
                    # If there are errors, render the form again with the error messages
                    return render(request, 'admin-employee-leave-insert.html', {"form": form})
            formInstance.save()
            messages.success(request, 'Inserted employee leave')
            return redirect('adminEmployeeLeaveOverview')
    else:
        form = EmployeeLeaveHistoryForm()
        return render(request, 'admin-employee-leave-insert.html', {"form":form})
    
@admin_role_required
def adminApproveLeave(request, pk):
    leaveRequest = EmployeeLeaveHistory.objects.filter(id=pk).get()
    if leaveRequest:
        employeeLeaveProfile = EmployeeLeave.objects.filter(id=leaveRequest.employeeLeave.id).get()
        if leaveRequest.leave_type == 'annual leave':
            employeeLeaveProfile.annual_leave -= leaveRequest.qty
            employeeLeaveProfile.save()
        elif leaveRequest.leave_type == 'childcare leave':
            employeeLeaveProfile.childcare_leave -= leaveRequest.qty
            employeeLeaveProfile.save()
        elif leaveRequest.leave_type == 'meternity leave':
            employeeLeaveProfile.maternity_leave -= leaveRequest.qty
            employeeLeaveProfile.save()
        elif leaveRequest.leave_type == 'paternity leave':
            employeeLeaveProfile.paternity_leave -= leaveRequest.qty
            employeeLeaveProfile.save()
        elif leaveRequest.leave_type == 'sick leave':
            employeeLeaveProfile.sick_leave -= leaveRequest.qty
            employeeLeaveProfile.save()
        elif leaveRequest.leave_type == 'unpaid leave':
            employeeLeaveProfile.unpaid_leave -= leaveRequest.qty
            employeeLeaveProfile.save()
        leaveRequest.status = EmployeeLeaveHistory.APPROVED
        leaveRequest.save()
        messages.success(request, 'Leave request approved')
        return redirect('adminEmployeeLeaveOverview')
    
@admin_role_required
def adminRejectLeave(request, pk):
    leaveRequest = EmployeeLeaveHistory.objects.filter(id=pk).get()
    if leaveRequest:
        leaveRequest.status = EmployeeLeaveHistory.REJECTED
        leaveRequest.save()
        messages.success(request, 'Leave request rejected')
        return redirect('adminEmployeeLeaveOverview')
    
@admin_role_required
def adminEmployeeLeaveDetail(request, pk):
    employeeLeaveProfile = EmployeeLeave.objects.filter(id=pk).get()
    employeeLeaveHistory = EmployeeLeaveHistory.objects.filter(employeeLeave=employeeLeaveProfile)
    return render(request, 'admin-employee-leave-detail.html', {"employeeLeaveProfile":employeeLeaveProfile, "employeeLeaveHistory": employeeLeaveHistory})

@employee_role_required
def employeeApplyLeave(request):
    if request.method == 'POST':
        form = EmployeeLeaveHistoryForm(request.POST, request.FILES)
        employeeLeaveProfile = EmployeeLeave.objects.filter(user=request.user).get()
        if form.is_valid():
            formInstance = form.save(commit=False)
            formInstance.employeeLeave = employeeLeaveProfile
            formInstance.status = EmployeeLeaveHistory.PENDING
            formInstance.entry = EmployeeLeaveHistory.SUBSTRACT

            #check if balance is sufficent to deduct 
            if formInstance.leave_type == 'annual leave' and employeeLeaveProfile.annual_leave - formInstance.qty < 0:
                form.add_error('leave_type', 'Insufficient annual leave')
            elif formInstance.leave_type == 'childcare leave' and employeeLeaveProfile.childcare_leave - formInstance.qty < 0:
                form.add_error('leave_type', 'Insufficient childcare leave')
            elif formInstance.leave_type == 'maternity leave' and employeeLeaveProfile.maternity_leave - formInstance.qty < 0:
                form.add_error('leave_type', 'Insufficient maternity leave')
            elif formInstance.leave_type == 'paternity leave' and employeeLeaveProfile.paternity_leave - formInstance.qty < 0:
                form.add_error('leave_type', 'Insufficient paternity leave')
            elif formInstance.leave_type == 'sick leave' and employeeLeaveProfile.sick_leave - formInstance.qty < 0:
                form.add_error('leave_type', 'Insufficient sick leave')
            elif formInstance.leave_type == 'unpaid leave' and employeeLeaveProfile.unpaid_leave - formInstance.qty < 0:
                form.add_error('leave_type', 'Insufficient unpaid leave')

            if form.errors:  # Check if there are any errors in the form
                    # If there are errors, render the form again with the error messages
                return render(request, 'employee-apply-leave.html', {"form": form, "employeeLeaveProfile":employeeLeaveProfile})
            formInstance.save()
            messages.success(request, 'Leave applied, awaiting for approval')
            return redirect('employeeIndex')            
    else:
        form = EmployeeLeaveHistoryForm()
        employeeLeaveProfile = EmployeeLeave.objects.filter(user=request.user).get()
        return render(request, 'employee-apply-leave.html', {"form":form, "employeeLeaveProfile":employeeLeaveProfile})

@employee_role_required
def employeeLeaveOverview(request):
    employeeLeaveProfile = EmployeeLeave.objects.filter(user=request.user).get()
    AllLeaveRequest = EmployeeLeaveHistory.objects.filter(employeeLeave=employeeLeaveProfile)
    return render(request, 'employee-leave-overview.html', {"employeeLeaveProfile":employeeLeaveProfile, "AllLeaveRequest":AllLeaveRequest})

@admin_role_required
def adminAddFrontendEmployee(request):
    if request.method == 'POST':
        form = EmployeeFrontendForm(request.POST, request.FILES)
        if form.is_valid():
            form_instance = form.save(commit=False)

            image_field = form.cleaned_data['profile_picture']
            profile_picture = Image.open(image_field)

            if profile_picture != (500, 500):
                profile_picture = profile_picture.resize((500,500))

                # Convert RGBA images to RGB before saving as JPEG
                if profile_picture.mode == 'RGBA':
                    profile_picture = profile_picture.convert('RGB')
                    
                #convet the resized image back to ImageField
                thumb_io = io.BytesIO()
                profile_picture.save(thumb_io, format=profile_picture.format or 'JPEG')
                file_name = image_field.name.split('.')[0] + '.jpeg'  # Making an assumption about the file name here
                form_instance.profile_picture.save(file_name, ContentFile(thumb_io.getvalue()), save=False)
            form_instance.save()
            messages.success(request, 'Employee frontend profile created')
            return redirect('adminAddFrontendEmployee')
        else:
            messages.success(request, 'Failed to create employee frontend profile', {"form":form})
    else:
        form = EmployeeFrontendForm()
        context = {
            'form':form
        }
        return render(request, 'admin-add-frontend-employee.html', context)
  
@admin_role_required
def adminFrontendEmployeeProfileOverview(request):
    profiles = EmployeeFrontendProfile.objects.all().order_by('-created_at')
    paginator = Paginator(profiles, 12)

    page = request.GET.get('page')

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'admin-frontend-employee-profile-overview.html', {'objects':objects})

@admin_role_required
def adminDeleteFrontendEmployeeProfile(request, pk):
    employeeProfile = EmployeeFrontendProfile.objects.filter(id=pk).get()
    if employeeProfile:
        employeeProfile.delete()
        messages.success(request, 'Deleted frontend employee profile')
        return redirect('adminFrontendEmployeeProfileOverview')
    else:
        messages.success(request, 'Failed to delete frontend employee profile')
        return redirect('adminFrontendEmployeeProfileOverview')

@admin_role_required
def adminEditFrontendEmployeeProfile(request, pk):
    try:
        employeeProfile = EmployeeFrontendProfile.objects.filter(id=pk).get()
    except:
        messages.error(request, 'Error in getting frontend employee profile')
        return redirect('adminFrontendEmployeeProfileOverview')
    
    if request.method == 'POST':
        form = EmployeeFrontendForm(request.POST, request.FILES, instance=employeeProfile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Frontend employee profile updated')
            return redirect('adminFrontendEmployeeProfileOverview')
    else:
        form = EmployeeFrontendForm(instance=employeeProfile)
        return render(request, 'admin-edit-frontend-employee-profile.html', {"form":form})