from django.shortcuts import render, redirect, get_object_or_404
from administration.decorator import employee_role_required, admin_role_required
from django.contrib import messages
from administration.models import Accounts, AccountProfiles
from django.core.paginator import Paginator, EmptyPage
from .forms import CustomerProfileForm, CustomerNotesForm, CreditHistoryForm, PackageForm, PackageHistoryForm
from .models import CustomerNotes, CustomerProfile, CreditHistory, Package, PackageHistory
from pos.models import SalesTransaction, SaleServices
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from jsignature.utils import draw_signature

# Create your views here.
@admin_role_required
def adminCreateCustomer(request):
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer registered')
        else:
            messages.success(request, 'Unable to register customer')
        return redirect('adminCreateCustomer')
    else:
        form = CustomerProfileForm()
        return render(request, 'admin-create-customer.html', {"form":form})


@admin_role_required
def adminCustomerOverview(request):
    customers = CustomerProfile.objects.all()

    return render(request, 'admin-customer-overview.html', {"customers":customers})

@admin_role_required
def adminCustomerDetails(request, pk):

    customerDetails = CustomerProfile.objects.filter(id=pk).get()
    creditHistory = CreditHistory.objects.filter(customer_profile_id=pk).order_by('-created_at')
    noteHistory = CustomerNotes.objects.filter(customer_profile_id=pk).order_by('-created_at')
    packages = Package.objects.filter(customer_profile_id=pk).order_by('-created_at')
    salesTransactions = SalesTransaction.objects.filter(customer=customerDetails.id)

    return render(request, 'admin-customer-details.html', {"customerDetails":customerDetails, "creditHistory":creditHistory, "noteHistory":noteHistory, "packages":packages, "salesTransactions":salesTransactions})


@admin_role_required
def adminEditCustomerDetails(request, pk):
    customerDetails = CustomerProfile.objects.filter(id=pk).get()

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customerDetails)
        notesForm = CustomerNotesForm(request.POST)

        if notesForm.is_valid():
            noteInstance = notesForm.save(commit=False)
            noteInstance.customer_profile = customerDetails #Set the customer profile FK
            print(noteInstance.customer_profile)
            noteInstance.save()
            messages.success(request, "Notes added")
        if form.is_valid():
            form.save()
            messages.success(request, "Updated customer profile")
        return redirect('adminEditUserDetails', pk=pk)

    else:
        #edit form
        form = CustomerProfileForm(instance=customerDetails)
        notesForm = CustomerNotesForm()

    return render(request, 'admin-edit-customer.html', {"form":form, "notesForm":notesForm})

@admin_role_required
def adminDeleteNote(request, pk, customerpk):
    deleteNote = CustomerNotes.objects.filter(id=pk).get()
    if deleteNote:
        deleteNote.delete()
        messages.success(request, 'Note deleted')
        return redirect('adminUserDetails', pk=customerpk)

@admin_role_required
def adminDeleteCustomer(request, pk):
    customerProfile = CustomerProfile.objects.filter(id=pk)

    if customerProfile:
        customerProfile.delete()
        messages.success(request, 'Customer profile deleted')
        return redirect('adminCustomerOverview')
    

@admin_role_required
def adminVoucherCustomer(request):
    return render(request, 'admin-voucher-customer.html')


@admin_role_required
def adminCreditCustomer(request):
    if request.method == 'POST':
        form = CreditHistoryForm(request.POST)
        if form.is_valid():
            #Get customer record
            creditInstance = form.save(commit=False)
            customer = creditInstance.customer_profile
            print(creditInstance.entry)
            if creditInstance.entry == 'debit':
                if customer.credit - creditInstance.amount >= 0:
                    customer.credit -= creditInstance.amount
                    creditInstance.save()
                    customer.save()
                    messages.success(request, 'Debit customer successfully')
                else:
                    messages.success(request, 'Not enough credit')
            else:
                customer.credit += creditInstance.amount
                creditInstance.save()
                customer.save()
                messages.success(request, 'Credit customer successfully')
        return redirect('adminCreditCustomer')
    else:
        form = CreditHistoryForm()
        return render(request, 'admin-credit-customer.html', {"form":form})

@admin_role_required
def adminIssueVoucherCustomer(request):
    if request.method =='POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            formInstance = form.save(commit=False)
            formInstance.balanceQty = formInstance.qty
            formInstance.save()
            messages.success(request, 'Package created')
        return redirect('adminIssueVoucherCustomer')
    else:
        form = PackageForm()
        return render(request, 'admin-issue-voucher-customer.html', {"form":form})

@admin_role_required
def adminCustomerVoucherDetail(request, pk):
    packageHistory = PackageHistory.objects.filter(package_id=pk)
    package = Package.objects.filter(id=pk).get()
    return render(request, 'admin-customer-voucher-details.html', {"packageHistory": packageHistory, "package":package})

@admin_role_required
def adminDeductVoucher(request, pk):
    if request.method == 'POST':
        form = PackageHistoryForm(request.POST)
        if form.is_valid():
            packageHistoryInstance = form.save(commit=False)
            package = Package.objects.filter(id=packageHistoryInstance.package.id).get()
            if packageHistoryInstance.entry == 'debit' and package.balanceQty - packageHistoryInstance.qty < 0:
                #throw form error
                form.add_error('qty', 'Insufficient balance to perform debit.')
                return render(request, 'admin-deduct-voucher-customer.html', {"form": form, "package": package})
            if packageHistoryInstance.entry == 'debit':
                package.balanceQty -= packageHistoryInstance.qty
                package.save()
            if packageHistoryInstance.entry == 'credit':
                package.balanceQty += packageHistoryInstance.qty
                package.save()
            form.save()
            messages.success(request, 'Package updated')
            return redirect('adminCustomerVoucherDetail', pk=pk)
        else:
            return redirect('adminCustomerVoucherDetail', pk=pk)
    else:
        package = Package.objects.filter(id=pk).get()
        initial_data = {'package':package}
        form = PackageHistoryForm(initial=initial_data)
        return render(request, 'admin-deduct-voucher-customer.html', {"form":form, "package":package})
    
@admin_role_required
def handle_customer_profile(request):
    if request.method == 'GET':
        customer_profile = request.GET.get('customer_profile', '')
        customer_credit = CustomerProfile.objects.filter(id=customer_profile).get()
        customer_data = {
            'c_credit' : customer_credit.credit,
        }

        return JsonResponse(customer_data)
    else:
        return JsonResponse({'error':'Customer profile is empty!'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)