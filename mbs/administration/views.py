import math
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from .models import Accounts, Product, ProductHistory, ContactForm, FrontendBanner
from pos.models import SalesTransaction
from pos.forms import SendEmailReceiptForm
from customer.models import CustomerProfile
from .decorator import admin_role_required
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.db.models import Sum
from .forms import FrontEndBannerForm
from PIL import Image
from django.core.files.base import ContentFile
import io
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse


# Create your views here.
from .forms import EmailUserCreationForm, AccountProfileForm, AccountForm, OptionalPasswordChangeForm, AccountEmailForm, ProductForm, ProductHistoryForm

@admin_role_required
def adminIndex(request):
    #extract user
    user = request.user

    #extract revenue, transactions, customers and new feedbacks
    revenue = SalesTransaction.objects.filter(created_at__contains=date.today()).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
    transactionCount = SalesTransaction.objects.filter(created_at__contains=date.today()).count()
    customersCount = CustomerProfile.objects.all().count()
    feddbackCount = ContactForm.objects.filter(created_at__contains=date.today()).count()

    revenue = math.floor(revenue * 100) /100 if revenue is not None else 0
    transactionCount = transactionCount if transactionCount is not None else 0
    customersCount = customersCount if customersCount is not None else 0
    feddbackCount = feddbackCount if feddbackCount is not None else 0


    salesTransactions = SalesTransaction.objects.filter(created_at__contains=date.today())
    emailForm = SendEmailReceiptForm()
    today = date.today()
    yesterday = today - timedelta(days=1)

    context = {
        "user":user,
        "revenue":revenue,
        "transactionCount":transactionCount,
        "customersCount":customersCount,
        "feddbackCount":feddbackCount,
        "emailForm" : emailForm,
        "salesTransactions":salesTransactions,
        "today": today,
        "yesterday":yesterday,
    }

    return render(request, 'index.html', context)

@admin_role_required
@login_required
def adminProfile(request):
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
                    return redirect("adminIndex")
                else:
                    passwordForm.add_error('new_password2', "Passwords do not match.")
            else:
                passwordForm.add_error('old_password', "Your old password was entered incorrectly. Please enter it again.")
        else:
            print("Password Form Errors:", passwordForm.errors)
        messages.success(request, 'Profile updated')
        return redirect("adminIndex")
    else:
        #extract user and Account form 
        user = request.user
        accountForm = AccountEmailForm(instance=user)
        passwordForm = OptionalPasswordChangeForm(request.user)
        #Get user account profile instant & pre-fill the form 
        profile_instance = user.accountprofile
        profileForm = AccountProfileForm(instance=profile_instance)
        return render(request, 'administration-profile.html', {"user":user, "profileForm":profileForm, "accountForm":accountForm, "passwordForm":passwordForm})

@admin_role_required
def adminRegister(request):
    if request.method == 'POST':
        registerForm = EmailUserCreationForm(request.POST)
        profileForm = AccountProfileForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save()
            #register account profile
            profile = profileForm.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "employee account registered.")
            return redirect("adminIndex")
        else:
            messages.error(request,"Unable to register employee")
            return render(request, 'authentication-signup.html', {'registerForm':registerForm, 'profileForm':profileForm})

    else:
        registerForm = EmailUserCreationForm()
        profileForm = AccountProfileForm()
    return render(request, 'authentication-signup.html', {'registerForm':registerForm, 'profileForm':profileForm})

def adminLogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.role == Accounts.EMPLOYEE:
                return redirect("employeeIndex")
            elif user.role== Accounts.ADMIN: 
                return redirect("adminIndex")
        else:
            context = {'message': "Unable to login, please try again.."}
            return render(request, 'authentication-signin.html', context)
    return render(request, 'authentication-signin.html')

def logout_request(request):
    logout(request)
    return redirect("login")

@admin_role_required
def adminProductOverview(request):
    products = Product.objects.all()
    return render(request, 'admin-product-overview.html',{"products":products})

@admin_role_required
def adminProductRegister(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product registered')
        return redirect('adminProductOverview')
    else:   
        form = ProductForm()
        return render(request, 'admin-add-product.html',{"form":form})
    
@admin_role_required
def adminDeleteProduct(request, pk):
    product = Product.objects.filter(id=pk)
    if product:
        product.delete() 
        messages.success(request, 'Product deleted')
        return redirect('adminProductOverview')
    else:
        messages.success(request, 'Unable to delete product')
        return redirect('adminProductOverview')
    
@admin_role_required
def adminProductDetails(request, pk):
    product = Product.objects.filter(id=pk).get()
    if product:
        productHistory = ProductHistory.objects.filter(product_id=product.id)
        return render(request, 'admin-product-details.html', {"product":product, "productHistory":productHistory})
    else:
        return redirect('adminProductOverview')
    
@admin_role_required
def adminEditProduct(request, pk):
    if request.method == 'POST':
        product = Product.objects.filter(id=pk).get()
        form = ProductForm(request.POST, request.FILES, instance=product)
        formHistory = ProductHistoryForm(request.POST)
        if form.is_valid() and formHistory.is_valid():
            productInstance = form.save(commit=False)
            productHistoryInstance = formHistory.save(commit=False)
            #check qty to determine if > or <
            if productHistoryInstance.entry == ProductHistory.ADD: 
                productInstance.qty += productHistoryInstance.editQty
            elif productHistoryInstance.entry == ProductHistory.SUBSTRACT: 
                if productInstance.qty - productHistoryInstance.editQty < 0:
                    formHistory.add_error('editQty', 'Stock quantity cannot fall below zero')
                    messages.success(request, 'Quantity error')
                    return render(request, 'admin-edit-product.html', {"form":form, "formHistory":formHistory})
                productInstance.qty -= productHistoryInstance.editQty
            
            productHistoryInstance.product = product
            #saving both forms
            productInstance.save()
            productHistoryInstance.save()
            messages.success(request, 'product updated')
            return redirect('adminProductOverview')
    else:
        formHistory = ProductHistoryForm()
        product = Product.objects.filter(id=pk).get()
        form = ProductForm(instance=product)
        return render(request, 'admin-edit-product.html', {"form":form, "formHistory":formHistory})
    
@admin_role_required
def adminFeedbackOverview(request):
    feedbacks = ContactForm.objects.all()
    context = {
        'feedbacks': feedbacks,
    }
    return render(request, 'admin-feedback-overview.html', context)

@admin_role_required
def adminFeedbackDelete(request, pk):
    feedback = ContactForm.objects.filter(id=pk)
    if feedback:
        feedback.delete()
        messages.success(request, 'Feedback deleted.')
        return redirect('adminFeedbackOverview')
    else:
        messages.success(request, 'Error in deleting feedback')
        return redirect('adminFeedbackOverview')

@admin_role_required
def adminAddFrontendBanner(request):
    if request.method == 'POST':
        form = FrontEndBannerForm(request.POST, request.FILES)
        if form.is_valid():
            form_instance = form.save(commit=False)

            image_field = form.cleaned_data['image']
            image = Image.open(image_field)

            if image != (500, 500):
                image = image.resize((500,500))

                # Convert RGBA images to RGB before saving as JPEG
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                    
                #convet the resized image back to ImageField
                thumb_io = io.BytesIO()
                image.save(thumb_io, format=image.format or 'JPEG')
                file_name = image_field.name.split('.')[0] + '.jpeg'  # Making an assumption about the file name here
                form_instance.image.save(file_name, ContentFile(thumb_io.getvalue()), save=False)
            form_instance.save()
            messages.success(request, 'Banner registered')
            return redirect('adminAddFrontendBanner')
        else:
            context= {
                'form':form,
            }
            messages.success(request, 'Failed to register banner')
            return render(request, 'admin-add-frontendbanner.html', context)
    else:
        form = FrontEndBannerForm()
        context = {
            'form':form
        }
        return render(request, 'admin-add-frontendbanner.html', context)
    

@admin_role_required
def adminFrontendBannerOverview(request):
    banners = FrontendBanner.objects.all().order_by('-created_at')
    paginator = Paginator(banners, 12)

    page = request.GET.get('page')

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, 'admin-frontendBanner-overview.html', {'objects':objects})

@admin_role_required
def handle_frontend_select(request):
    frontendID = request.GET.get('frontendId')
    try:
        frontendObj = FrontendBanner.objects.get(id=frontendID)
        if frontendObj.selected:
            frontendObj.selected = False
            frontendObj.save()
            data = {
                'success': 'unselected'
            }
            return JsonResponse(data)
        else:
            frontendObj.selected = True
            frontendObj.save()
            data = {
                'success': 'selected'
            }
            return JsonResponse(data)
    except FrontendBanner.DoesNotExist:
        data = {
            'success': False
        }
        return JsonResponse(data)
    
@admin_role_required
def adminEditFrontendBanner(request, pk):
    try:
        frontendBanner = FrontendBanner.objects.get(id=pk)
    except FrontendBanner.DoesNotExist:
        messages.error(request, 'Error in getting frontend banner')
        return redirect('adminFrontendBannerOverview')

    if request.method == 'POST':
        # You need to provide the instance you want to update to the form
        # You also need to pass request.FILES if the form has FileFields or ImageFields
        form = FrontEndBannerForm(request.POST, request.FILES, instance=frontendBanner)
        if form.is_valid():
            form.save()
            messages.success(request, 'Frontend banner updated successfully')
            return redirect('adminFrontendBannerOverview')
    else:
        form = FrontEndBannerForm(instance=frontendBanner)

    context = {
        "form": form,
    }
    return render(request, 'admin-edit-frontendBanner.html', context)

@admin_role_required
def adminDeleteFrontendBanner(request, pk):
    try:
        frontendBanner = FrontendBanner.objects.get(id=pk)
    except FrontendBanner.DoesNotExist:
        messages.error(request, 'Error in getting frontend banner')
        return redirect('adminFrontendBannerOverview')
    
    if frontendBanner:
        frontendBanner.delete();
        messages.success(request, 'Frontend banner deleted')
        return redirect('adminFrontendBannerOverview')

