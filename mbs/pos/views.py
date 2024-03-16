from django.shortcuts import render, redirect
from .models import SalesTransaction, SaleServices
from .forms import SalesTransactionForm, SaleServiceFormset, SelectDatesForm, SendEmailReceiptForm
from django.contrib import messages
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta, date, datetime
from administration.decorator import employee_role_required, admin_role_required
from django.forms import inlineformset_factory
import json
import math
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


# Create your views here.

@admin_role_required
def startPos(request):
    if request.method == 'POST':
        form = SalesTransactionForm(request.POST)
        sale_service_formset = SaleServiceFormset(request.POST)
        form.formset = sale_service_formset
        if form.is_valid():
            sales_transaction = form.save()
            sale_service_formset.instance = sales_transaction
            print(sale_service_formset)
            if sale_service_formset.is_valid():
                sale_services = sale_service_formset.save()

            messages.success(request, 'Transaction created')
            return redirect('startPos') 
        else:
            messages.success(request,'Transaction failed, please try again..')
            #Display revenue 
            today = timezone.now().date()
            yesterday = today - timedelta(days=1)

            # Total revenue excluding REFUND
            todayRevenue = SalesTransaction.objects.filter(created_at__contains=today).exclude(payment_type=SalesTransaction.REFUND).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
            todayRevenue = todayRevenue if todayRevenue is not None else 0

            yesterdayRevenue = SalesTransaction.objects.filter(created_at__contains=yesterday).exclude(payment_type=SalesTransaction.REFUND).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
            yesterdayRevenue = yesterdayRevenue if yesterdayRevenue is not None else 0

            percentageRevenue = 0.0
            if todayRevenue and yesterdayRevenue:
                percentageRevenue = todayRevenue / yesterdayRevenue
                percentageRevenue = percentageRevenue - 1
                percentageRevenue = percentageRevenue * 100
            

            # Breakdown by payment types
            todayCash = SalesTransaction.objects.filter(created_at__contains=today, payment_type=SalesTransaction.CASH).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
            todayCash = todayCash if todayCash is not None else 0

            todayPaynow = SalesTransaction.objects.filter(created_at__contains=today, payment_type=SalesTransaction.PAYNOW).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
            todayPaynow = todayPaynow if todayPaynow is not None else 0

            todayCreditCard = SalesTransaction.objects.filter(created_at__contains=today, payment_type=SalesTransaction.CREDIT_CARD).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
            todayCreditCard = todayCreditCard if todayCreditCard is not None else 0

            todayNets = SalesTransaction.objects.filter(created_at__contains=today, payment_type=SalesTransaction.NETS).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
            todayNets = todayNets if todayNets is not None else 0

            todayGrab = SalesTransaction.objects.filter(created_at__contains=today, payment_type=SalesTransaction.GRAB).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
            todayGrab = todayGrab if todayGrab is not None else 0

            todayPackage = SalesTransaction.objects.filter(created_at__contains=today, payment_type=SalesTransaction.PACKAGE).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
            todayPackage = todayPackage if todayPackage is not None else 0

            todayInStoreCredit = SalesTransaction.objects.filter(created_at__contains=today, payment_type=SalesTransaction.CREDITSALES).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
            todayInStoreCredit = todayInStoreCredit if todayInStoreCredit is not None else 0

            todayRefund = SalesTransaction.objects.filter(created_at__contains=today, payment_type=SalesTransaction.REFUND).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
            todayRefund = todayRefund if todayRefund is not None else 0

            todayBeauty = SaleServices.objects.filter(created_at__contains=today, department=SaleServices.BEAUTY).aggregate(total_revenue=Sum('service_price'))['total_revenue']
            todayBeauty = todayBeauty if todayBeauty is not None else 0

            todayHair = SaleServices.objects.filter(created_at__contains=today, department=SaleServices.HAIR).aggregate(total_revenue=Sum('service_price'))['total_revenue']
            todayHair = todayHair if todayHair is not None else 0

            todayHealth = SaleServices.objects.filter(created_at__contains=today, department=SaleServices.HEALTH).aggregate(total_revenue=Sum('service_price'))['total_revenue']
            todayHealth = todayHealth if todayHealth is not None else 0

            todayHairProduct = SaleServices.objects.filter(created_at__contains=today, department=SaleServices.HAIRPRODUCT).aggregate(total_revenue=Sum('service_price'))['total_revenue']
            todayHairProduct = todayHairProduct if todayHairProduct is not None else 0

            todayBeautyProduct = SaleServices.objects.filter(created_at__contains=today, department=SaleServices.BEAUTYPRODUCT).aggregate(total_revenue=Sum('service_price'))['total_revenue']
            todayBeautyProduct = todayBeautyProduct if todayBeautyProduct is not None else 0

            todayPackageSales = SaleServices.objects.filter(created_at__contains=today, department=SaleServices.PACKAGESALES).aggregate(total_revenue=Sum('service_price'))['total_revenue']
            todayPackageSales = todayPackageSales if todayPackageSales is not None else 0

            todayCreditSales = SaleServices.objects.filter(created_at__contains=today, department=SaleServices.CREDITSALES).aggregate(total_revenue=Sum('service_price'))['total_revenue']
            todayCreditSales = todayCreditSales if todayCreditSales is not None else 0


            context = {
                'todayRevenueValue': math.ceil(todayRevenue * 100) / 100.0,
                'todayCash': math.ceil(todayCash * 100) / 100.0,
                'todayPaynow': math.ceil(todayPaynow * 100) / 100.0,
                'todayCreditCard': math.ceil(todayCreditCard * 100) / 100.0,
                'todayNets': math.ceil(todayNets * 100) / 100.0,
                'todayGrab': math.ceil(todayGrab * 100) / 100.0,
                'todayPackage': math.ceil(todayPackage * 100) / 100.0,
                'todayInStoreCredit': math.ceil(todayInStoreCredit * 100) / 100.0,
                'todayRefund': math.ceil(todayRefund * 100) / 100.0,
                'form': form,
                'sale_service_formset': sale_service_formset,
                'percentageRevenue' : percentageRevenue,
                'todayBeauty': math.ceil(todayBeauty * 100) / 100.0,
                'todayHair': math.ceil(todayHair * 100) / 100.0,
                'todayHealth': math.ceil(todayHealth * 100) / 100.0,
                'todayHairProduct': math.ceil(todayHairProduct * 100) / 100.0,
                'todayBeautyProduct': math.ceil(todayBeautyProduct * 100) / 100.0,
                'todayPackageSales': math.ceil(todayPackageSales * 100) / 100.0,
                'todayCreditSales': math.ceil(todayCreditSales * 100) / 100.0,
            }

            return render(request, 'pos-startpos.html', context)
    else:
        #Display revenue 
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        # Total revenue excluding REFUND
        todayRevenue = SalesTransaction.objects.filter(created_at__contains=today).exclude(payment_type=SalesTransaction.REFUND).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
        todayRevenue = todayRevenue if todayRevenue is not None else 0

        yesterdayRevenue = SalesTransaction.objects.filter(created_at__contains=yesterday).exclude(payment_type=SalesTransaction.REFUND).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
        yesterdayRevenue = yesterdayRevenue if yesterdayRevenue is not None else 0


        percentageRevenue = 0.0
        if todayRevenue and yesterdayRevenue:
            percentageRevenue = todayRevenue / yesterdayRevenue
            percentageRevenue = percentageRevenue - 1
            percentageRevenue = percentageRevenue * 100
        

        # Breakdown by payment types
        todayCash = SalesTransaction.objects.filter(created_at__contains=today, payment_type=SalesTransaction.CASH).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
        todayCash = todayCash if todayCash is not None else 0

        todayPaynow = SalesTransaction.objects.filter(created_at__contains=today, payment_type=SalesTransaction.PAYNOW).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
        todayPaynow = todayPaynow if todayPaynow is not None else 0

        todayCreditCard = SalesTransaction.objects.filter(created_at__contains=today, payment_type=SalesTransaction.CREDIT_CARD).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
        todayCreditCard = todayCreditCard if todayCreditCard is not None else 0

        todayNets = SalesTransaction.objects.filter(created_at__contains=today, payment_type=SalesTransaction.NETS).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
        todayNets = todayNets if todayNets is not None else 0

        todayGrab = SalesTransaction.objects.filter(created_at__contains=today, payment_type=SalesTransaction.GRAB).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
        todayGrab = todayGrab if todayGrab is not None else 0

        todayPackage = SalesTransaction.objects.filter(created_at__contains=today, payment_type=SalesTransaction.PACKAGE).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
        todayPackage = todayPackage if todayPackage is not None else 0

        todayInStoreCredit = SalesTransaction.objects.filter(created_at__contains=today, payment_type=SalesTransaction.CREDITSALES).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
        todayInStoreCredit = todayInStoreCredit if todayInStoreCredit is not None else 0

        todayRefund = SalesTransaction.objects.filter(created_at__contains=today, payment_type=SalesTransaction.REFUND).aggregate(total_revenue=Sum('grand_total'))['total_revenue']
        todayRefund = todayRefund if todayRefund is not None else 0

        todayBeauty = SaleServices.objects.filter(created_at__contains=today, department=SaleServices.BEAUTY).aggregate(total_revenue=Sum('service_price'))['total_revenue']
        todayBeauty = todayBeauty if todayBeauty is not None else 0

        todayHair = SaleServices.objects.filter(created_at__contains=today, department=SaleServices.HAIR).aggregate(total_revenue=Sum('service_price'))['total_revenue']
        todayHair = todayHair if todayHair is not None else 0

        todayHealth = SaleServices.objects.filter(created_at__contains=today, department=SaleServices.HEALTH).aggregate(total_revenue=Sum('service_price'))['total_revenue']
        todayHealth = todayHealth if todayHealth is not None else 0

        todayHairProduct = SaleServices.objects.filter(created_at__contains=today, department=SaleServices.HAIRPRODUCT).aggregate(total_revenue=Sum('service_price'))['total_revenue']
        todayHairProduct = todayHairProduct if todayHairProduct is not None else 0

        todayBeautyProduct = SaleServices.objects.filter(created_at__contains=today, department=SaleServices.BEAUTYPRODUCT).aggregate(total_revenue=Sum('service_price'))['total_revenue']
        todayBeautyProduct = todayBeautyProduct if todayBeautyProduct is not None else 0

        todayPackageSales = SaleServices.objects.filter(created_at__contains=today, department=SaleServices.PACKAGESALES).aggregate(total_revenue=Sum('service_price'))['total_revenue']
        todayPackageSales = todayPackageSales if todayPackageSales is not None else 0

        todayCreditSales = SaleServices.objects.filter(created_at__contains=today, department=SaleServices.CREDITSALES).aggregate(total_revenue=Sum('service_price'))['total_revenue']
        todayCreditSales = todayCreditSales if todayCreditSales is not None else 0


        context = {
            'todayRevenueValue': math.ceil(todayRevenue * 100) / 100.0,
            'todayCash': math.ceil(todayCash * 100) / 100.0,
            'todayPaynow': math.ceil(todayPaynow * 100) / 100.0,
            'todayCreditCard': math.ceil(todayCreditCard * 100) / 100.0,
            'todayNets': math.ceil(todayNets * 100) / 100.0,
            'todayGrab': math.ceil(todayGrab * 100) / 100.0,
            'todayPackage': math.ceil(todayPackage * 100) / 100.0,
            'todayInStoreCredit': math.ceil(todayInStoreCredit * 100) / 100.0,
            'todayRefund': math.ceil(todayRefund * 100) / 100.0,
            'form': SalesTransactionForm(),
            'sale_service_formset': SaleServiceFormset(queryset=SaleServices.objects.none()),
            'percentageRevenue' : percentageRevenue,
            'todayBeauty': math.ceil(todayBeauty * 100) / 100.0,
            'todayHair': math.ceil(todayHair * 100) / 100.0,
            'todayHealth': math.ceil(todayHealth * 100) / 100.0,
            'todayHairProduct': math.ceil(todayHairProduct * 100) / 100.0,
            'todayBeautyProduct': math.ceil(todayBeautyProduct * 100) / 100.0,
            'todayPackageSales': math.ceil(todayPackageSales * 100) / 100.0,
            'todayCreditSales': math.ceil(todayCreditSales * 100) / 100.0,
        }

        return render(request, 'pos-startpos.html', context)

@admin_role_required
def adminTransactionsOverview(request):

    if request.method == 'POST':
        form = SelectDatesForm(request.POST)
        if form.is_valid():
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            employee = form.cleaned_data['employee']

            # Base query filters
            filters = {
                'created_at__range': (datetime.combine(startDate, datetime.min.time()), datetime.combine(endDate, datetime.max.time()))
            }
            filters2 = {
                'created_at__range': (datetime.combine(startDate, datetime.min.time()), datetime.combine(endDate, datetime.max.time()))
            }

            if employee:
                filters['user'] = employee
                filters2['sales_transaction__user'] = employee

            #Construct chart data (daily)
            dailyLabel = []
            dailyData = []
            dailyDate = timezone.now().date()
            for i in range(14):
                dailyData.append(SalesTransaction.objects.filter(created_at__contains=dailyDate).aggregate(total_revenue=Sum('grand_total'))['total_revenue'])
                dailyLabel.append(dailyDate.strftime('%Y-%m-%d'))
                dailyDate = dailyDate - timedelta(days=1)
            form = SelectDatesForm()

            #Construct chart data (department)
            departmentLabel = []
            departmentData = []

            salesTransactions = SalesTransaction.objects.filter(**filters).order_by('-created_at')
            today = timezone.now().date()
            yesterday = today - timedelta(days=1)

            #Hair
            departmentLabel.append('Hair')
            tempHair = SaleServices.objects.filter(**filters2, department=SaleServices.HAIR).aggregate(total_revenue=Sum('service_price'))['total_revenue']
            departmentData.append(math.ceil(tempHair * 100) / 100 if tempHair is not None else 0)
            #Beauty
            departmentLabel.append('Beauty')
            tempBeauty = SaleServices.objects.filter(**filters2, department=SaleServices.BEAUTY).aggregate(total_revenue=Sum('service_price'))['total_revenue']
            departmentData.append(math.ceil(tempBeauty * 100) / 100 if tempBeauty is not None else 0)
            #Health
            departmentLabel.append('Health')
            tempHealth = SaleServices.objects.filter(**filters2, department=SaleServices.HEALTH).aggregate(total_revenue=Sum('service_price'))['total_revenue']
            departmentData.append(math.ceil(tempHealth * 100) / 100 if tempHealth is not None else 0)
            #Hair product
            departmentLabel.append('Hair product')
            tempHairProduct = SaleServices.objects.filter(**filters2, department=SaleServices.HAIRPRODUCT).aggregate(total_revenue=Sum('service_price'))['total_revenue']
            departmentData.append(math.ceil(tempHairProduct * 100) / 100 if tempHairProduct is not None else 0)
            #Beauty product
            departmentLabel.append('Beauty product')
            tempBeautyProduct = SaleServices.objects.filter(**filters2, department=SaleServices.BEAUTYPRODUCT).aggregate(total_revenue=Sum('service_price'))['total_revenue']
            departmentData.append(math.ceil(tempBeautyProduct * 100) / 100 if tempBeautyProduct is not None else 0)
            #Package sales
            departmentLabel.append('Package sales')
            tempPackageSales = SaleServices.objects.filter(**filters2, department=SaleServices.PACKAGESALES).aggregate(total_revenue=Sum('service_price'))['total_revenue']
            departmentData.append(math.ceil(tempPackageSales * 100) / 100 if tempPackageSales is not None else 0)
            #Credit sales
            departmentLabel.append('Credit sales')
            tempCreditSales = SaleServices.objects.filter(**filters2, department=SaleServices.CREDITSALES).aggregate(total_revenue=Sum('service_price'))['total_revenue']
            departmentData.append(math.ceil(tempCreditSales * 100) / 100 if tempCreditSales is not None else 0)
            
            #Get all different types of payment 
            #total revenue
            total_revenue = SalesTransaction.objects.filter(**filters).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

            #cash
            cash = SalesTransaction.objects.filter(**filters, payment_type=SalesTransaction.CASH).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

            #paynow
            paynow = SalesTransaction.objects.filter(**filters, payment_type=SalesTransaction.PAYNOW).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

            #credit card
            creditCard = SalesTransaction.objects.filter(**filters, payment_type=SalesTransaction.CREDIT_CARD).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

            #Nets
            nets = SalesTransaction.objects.filter(**filters, payment_type=SalesTransaction.NETS).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

            #grab
            grab = SalesTransaction.objects.filter(**filters, payment_type=SalesTransaction.GRAB).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

            #package
            package = SalesTransaction.objects.filter(**filters, payment_type=SalesTransaction.PACKAGE).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

            #in store credit
            inStoreCredit = SalesTransaction.objects.filter(**filters, payment_type=SalesTransaction.CREDITSALES).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

            #refund
            refund = SalesTransaction.objects.filter(**filters, payment_type=SalesTransaction.REFUND).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

            #departmentHair
            departmentHair = SaleServices.objects.filter(**filters2, department=SaleServices.HAIR).aggregate(total_revenue=Sum('service_price'))['total_revenue']

            #departmentBeauty
            departmentBeauty = SaleServices.objects.filter(**filters2, department=SaleServices.BEAUTY).aggregate(total_revenue=Sum('service_price'))['total_revenue']

            #departmentHealth
            departmentHealth = SaleServices.objects.filter(**filters2, department=SaleServices.HEALTH).aggregate(total_revenue=Sum('service_price'))['total_revenue']

            #departmentHealth
            departmentHairProduct = SaleServices.objects.filter(**filters2, department=SaleServices.HAIRPRODUCT).aggregate(total_revenue=Sum('service_price'))['total_revenue']

            #departmentHealth
            departmentBeautyProduct = SaleServices.objects.filter(**filters2, department=SaleServices.BEAUTYPRODUCT).aggregate(total_revenue=Sum('service_price'))['total_revenue']

            #packageSales
            packageSales = SaleServices.objects.filter(**filters2, department=SaleServices.PACKAGESALES).aggregate(total_revenue=Sum('service_price'))['total_revenue']

            #creditSales
            creditSales = SaleServices.objects.filter(**filters2, department=SaleServices.CREDITSALES).aggregate(total_revenue=Sum('service_price'))['total_revenue']

            cash = cash if cash is not None else 0
            paynow = paynow if paynow is not None else 0
            creditCard = creditCard if creditCard is not None else 0
            nets = nets if nets is not None else 0
            grab = grab if grab is not None else 0
            package = package if package is not None else 0
            inStoreCredit = inStoreCredit if inStoreCredit is not None else 0
            refund = refund if refund is not None else 0
            departmentHair = departmentHair if departmentHair is not None else 0
            departmentBeauty = departmentBeauty if departmentBeauty is not None else 0
            departmentHealth = departmentHealth if departmentHealth is not None else 0
            total_revenue = total_revenue if total_revenue is not None else 0
            departmentHairProduct = departmentHairProduct if departmentHairProduct is not None else 0
            departmentBeautyProduct = departmentBeautyProduct if departmentBeautyProduct is not None else 0
            packageSales = packageSales if packageSales is not None else 0
            creditSales = creditSales if creditSales is not None else 0

            emailForm = SendEmailReceiptForm()

            context = {
                'salesTransactions':salesTransactions,
                'today' : today,
                'yesterday' : yesterday,
                'form': form,
                'dailyLabel' : json.dumps(dailyLabel),
                'dailyData' : json.dumps(dailyData),
                'departmentLabel' : json.dumps(departmentLabel),
                'departmentData': json.dumps(departmentData),
                'totalRevenue': math.ceil((total_revenue - refund) * 100) /100.0,
                'cash': math.ceil(cash * 100) /100.0,
                'paynow': math.ceil(paynow * 100) / 100.0,
                'creditCard':math.ceil(creditCard * 100) /100.0,
                'nets':math.ceil(nets * 100) /100.0,
                'grab':math.ceil(grab * 100) /100.0,
                'package':math.ceil(package * 100) /100.0,
                'inStoreCredit':math.ceil(inStoreCredit * 100) /100.0,
                'refund':math.ceil(refund * 100) /100.0,
                'departmentHair':math.ceil(departmentHair * 100) /100.0,
                'departmentBeauty':math.ceil(departmentBeauty * 100) /100.0,
                'departmentHealth':math.ceil(departmentHealth * 100) /100.0,
                'startDate':startDate,
                'endDate':endDate,
                'employee' : employee,
                'emailForm' : emailForm,
                'departmentBeautyProduct' : math.ceil(departmentBeautyProduct * 100) / 100,
                'departmentHairProduct' : math.ceil(departmentHairProduct * 100) / 100,
                'packageSales' : math.ceil(packageSales * 100) / 100,
                'creditSales' : math.ceil(creditSales * 100) / 100,

            }
            return render(request, 'pos-sales-history.html', context)
    else:
        #GET
        salesTransactions = SalesTransaction.objects.all().order_by('-created_at')
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        #Construct chart data (daily)
        dailyLabel = []
        dailyData = []
        dailyDate = timezone.now().date()
        for i in range(14):
            dailyData.append(SalesTransaction.objects.filter(created_at__contains=dailyDate).exclude(payment_type="credit sales").aggregate(total_revenue=Sum('grand_total'))['total_revenue'])
            dailyLabel.append(dailyDate.strftime('%Y-%m-%d'))
            dailyDate = dailyDate - timedelta(days=1)
        form = SelectDatesForm()

        #Construct chart data (department)
        departmentLabel = []
        departmentData = []
        #Hair
        departmentLabel.append('Hair')
        tempHair = SaleServices.objects.filter(department=SaleServices.HAIR).aggregate(total_revenue=Sum('service_price'))['total_revenue']
        departmentData.append(math.ceil(tempHair * 100) / 100 if tempHair is not None else 0)
        #Beauty
        departmentLabel.append('Beauty')
        tempBeauty = SaleServices.objects.filter(department=SaleServices.BEAUTY).aggregate(total_revenue=Sum('service_price'))['total_revenue']
        departmentData.append(math.ceil(tempBeauty * 100) / 100 if tempBeauty is not None else 0)
        #Health
        departmentLabel.append('Health')
        tempHealth = SaleServices.objects.filter(department=SaleServices.HEALTH).aggregate(total_revenue=Sum('service_price'))['total_revenue']
        departmentData.append(math.ceil(tempHealth * 100) / 100 if tempHealth is not None else 0)
        #HairProduct
        departmentLabel.append('Hair product')
        tempHairProduct = SaleServices.objects.filter(department=SaleServices.HAIRPRODUCT).aggregate(total_revenue=Sum('service_price'))['total_revenue']
        departmentData.append(math.ceil(tempHairProduct * 100) / 100 if tempHairProduct is not None else 0)
        #BeautyProduct
        departmentLabel.append('Beauty product')
        tempBeautyProduct = SaleServices.objects.filter(department=SaleServices.BEAUTYPRODUCT).aggregate(total_revenue=Sum('service_price'))['total_revenue']
        departmentData.append(math.ceil(tempBeautyProduct * 100) / 100 if tempBeautyProduct is not None else 0)
        #Package sales
        departmentLabel.append('Package sales')
        tempPackageSales = SaleServices.objects.filter(department=SaleServices.PACKAGESALES).aggregate(total_revenue=Sum('service_price'))['total_revenue']
        departmentData.append(math.ceil(tempPackageSales * 100) / 100 if tempPackageSales is not None else 0)
        #Credit sales
        departmentLabel.append('Credit sales')
        tempCreditSales = SaleServices.objects.filter(department=SaleServices.CREDITSALES).aggregate(total_revenue=Sum('service_price'))['total_revenue']
        departmentData.append(math.ceil(tempCreditSales * 100) / 100 if tempCreditSales is not None else 0)

        #Get all different types of payment 
        #total revenue
        total_revenue = SalesTransaction.objects.all().aggregate(total_revenue=Sum('grand_total'))['total_revenue']

        #cash
        cash = SalesTransaction.objects.filter(payment_type=SalesTransaction.CASH).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

        #paynow
        paynow = SalesTransaction.objects.filter(payment_type=SalesTransaction.PAYNOW).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

        #credit card
        creditCard = SalesTransaction.objects.filter(payment_type=SalesTransaction.CREDIT_CARD).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

        #Nets
        nets = SalesTransaction.objects.filter(payment_type=SalesTransaction.NETS).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

        #grab
        grab = SalesTransaction.objects.filter(payment_type=SalesTransaction.GRAB).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

        #package
        package = SalesTransaction.objects.filter(payment_type=SalesTransaction.PACKAGE).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

        #in store credit
        inStoreCredit = SalesTransaction.objects.filter(payment_type=SalesTransaction.CREDITSALES).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

        #refund
        refund = SalesTransaction.objects.filter(payment_type=SalesTransaction.REFUND).aggregate(total_revenue=Sum('grand_total'))['total_revenue']

        #departmentHair
        departmentHair = SaleServices.objects.filter(department=SaleServices.HAIR).aggregate(total_revenue=Sum('service_price'))['total_revenue']

        #departmentBeauty
        departmentBeauty = SaleServices.objects.filter(department=SaleServices.BEAUTY).aggregate(total_revenue=Sum('service_price'))['total_revenue']

        #departmentHealth
        departmentHealth = SaleServices.objects.filter(department=SaleServices.HEALTH).aggregate(total_revenue=Sum('service_price'))['total_revenue']

        #departmentHairProduct
        departmentHairProduct = SaleServices.objects.filter(department=SaleServices.HAIRPRODUCT).aggregate(total_revenue=Sum('service_price'))['total_revenue']

        #departmentHealth
        departmentBeautyProduct = SaleServices.objects.filter(department=SaleServices.BEAUTYPRODUCT).aggregate(total_revenue=Sum('service_price'))['total_revenue']

        #packageSales
        packageSales = SaleServices.objects.filter(department=SaleServices.PACKAGESALES).aggregate(total_revenue=Sum('service_price'))['total_revenue']

        #creditSales
        creditSales = SaleServices.objects.filter(department=SaleServices.CREDITSALES).aggregate(total_revenue=Sum('service_price'))['total_revenue']

        emailForm = SendEmailReceiptForm()

        cash = cash if cash is not None else 0
        paynow = paynow if paynow is not None else 0
        creditCard = creditCard if creditCard is not None else 0
        nets = nets if nets is not None else 0
        grab = grab if grab is not None else 0
        package = package if package is not None else 0
        inStoreCredit = inStoreCredit if inStoreCredit is not None else 0
        refund = refund if refund is not None else 0
        departmentHair = departmentHair if departmentHair is not None else 0
        departmentBeauty = departmentBeauty if departmentBeauty is not None else 0
        departmentHealth = departmentHealth if departmentHealth is not None else 0
        total_revenue = total_revenue if total_revenue is not None else 0
        departmentBeautyProduct = departmentBeautyProduct if departmentBeautyProduct is not None else 0
        departmentHairProduct = departmentHairProduct if departmentHairProduct is not None else 0
        packageSales = packageSales if packageSales is not None else 0
        creditSales = creditSales if creditSales is not None else 0

        context = {
            'salesTransactions':salesTransactions,
            'today' : today,
            'yesterday' : yesterday,
            'form': form,
            'dailyLabel' : json.dumps(dailyLabel),
            'dailyData' : json.dumps(dailyData),
            'departmentLabel' : json.dumps(departmentLabel),
            'departmentData': json.dumps(departmentData),
            'totalRevenue': math.ceil((total_revenue- refund) * 100) /100.0,
            'cash': math.ceil(cash * 100) /100.0,
            'paynow':math.ceil(paynow * 100) /100.0,
            'creditCard':math.ceil(creditCard * 100) /100.0,
            'nets':math.ceil(nets * 100) /100.0,
            'grab':math.ceil(grab * 100) /100.0,
            'package':math.ceil(package * 100) /100.0,
            'inStoreCredit':math.ceil(inStoreCredit * 100) /100.0,
            'refund':math.ceil(refund * 100) /100.0,
            'departmentHair':math.ceil(departmentHair * 100) /100.0,
            'departmentBeauty':math.ceil(departmentBeauty * 100) /100.0,
            'departmentHealth':math.ceil(departmentHealth * 100) /100.0,
            'emailForm' : emailForm,
            'departmentBeautyProduct' : math.ceil(departmentBeautyProduct * 100) / 100,
            'departmentHairProduct' : math.ceil(departmentHairProduct * 100) / 100,
            'packageSales' : math.ceil(packageSales * 100) / 100,
            'creditSales' : math.ceil(creditSales * 100) / 100,

        }
        return render(request, 'pos-sales-history.html', context)

@admin_role_required
def adminViewTransactionDetails(request, pk):
    salesTransaction = SalesTransaction.objects.filter(id=pk).get()
    transactionHistory = SaleServices.objects.filter(sales_transaction=pk)
    context={
        'salesTransaction' : salesTransaction,
        'transactionHistory' : transactionHistory
    }
    return render(request, 'pos-sales-transaction-details.html', context)

@admin_role_required
def adminEditTransaction(request, pk):
    try:
        salesTransaction = SalesTransaction.objects.get(id=pk)
    except SalesTransaction.DoesNotExist:
        return redirect('adminTransactionsOverview')
    
    if request.method == "POST":
        # Manipulate POST data
        post_data = request.POST.copy()  # Create a mutable copy
        total_forms = int(post_data.get('saleservices_set-TOTAL_FORMS'))
        for form_idx in range(total_forms):
            delete_key = f"saleservices_set-{form_idx}-DELETE"
            if delete_key in post_data and post_data[delete_key] == 'on':
                # If DELETE is ticked, clear the data for this form
                post_data[f"saleservices_set-{form_idx}-department"] = 'hair'
                post_data[f"saleservices_set-{form_idx}-service_name"] = 'dummy-value'
                post_data[f"saleservices_set-{form_idx}-service_price"] = '99.99'

        form = SalesTransactionForm(post_data, instance=salesTransaction)
        sale_service_formset = SaleServiceFormset(post_data, instance=salesTransaction)
        form.formset = sale_service_formset

        form_is_valid = form.is_valid()
        
        all_forms_valid = True
        for index, service_form in enumerate(sale_service_formset):
            if not service_form.is_valid():
                all_forms_valid = False
                break
            if service_form.cleaned_data.get('DELETE'):
                continue

        if form_is_valid and all_forms_valid:
            form.save()

            # Process individual service forms
            for service_form in sale_service_formset:
                # Process individual service forms
                for service_form in sale_service_formset:
                    # Check for deletion
                    if service_form.cleaned_data.get('DELETE'):
                        service_instance = service_form.instance
                        if service_instance.pk:  # If this is a saved instance, delete it
                            service_instance.delete()
                    else:
                        # If there's an ID, it's an update
                        if service_form.cleaned_data.get('id'):
                            service_form.save()
                        else:
                            # Create operation
                            new_service = service_form.save(commit=False)
                            new_service.sales_transaction = salesTransaction
                            new_service.save()

            return redirect('adminTransactionsOverview')
    else:
        form = SalesTransactionForm(instance=salesTransaction)
        sale_service_formset = SaleServiceFormset(instance=salesTransaction)

    context = {
        'form': form,
        'sale_service_formset': sale_service_formset,
    }
    
    return render(request, 'pos-edit-transaction.html', context)


@admin_role_required
def generateTransactionReceipt(request, pk):
    saleServices = SaleServices.objects.filter(sales_transaction=pk)
    saleTransaction = SalesTransaction.objects.filter(id=pk).get()
    print(saleTransaction.id)
    context = {
        'today' : timezone.now().date(),
        'saleServices' : saleServices,
        'saleTransaction' :saleTransaction,
    }
    return render(request, 'pos-email-receipt.html', context)

@admin_role_required
def send_email_receipt(request):
    if request.method == 'POST':
        emailForm = SendEmailReceiptForm(request.POST)
        email = "nil"
        pk = ""
        if emailForm.is_valid():
            email = emailForm.cleaned_data['email_address']
            pk = emailForm.cleaned_data['receipt_pk']
        if pk:
            saleServices = SaleServices.objects.filter(sales_transaction=pk)
            saleTransaction = SalesTransaction.objects.filter(id=pk).get()
        
        context = {
            'today' : timezone.now().date(),
            'saleServices' : saleServices,
            'saleTransaction' :saleTransaction,
        }

        html_message = render_to_string('pos-email-receipt.html', context)

        send_mail(
            'Melon Beauty Salon Receipt',       # subject
            'Please ensure that your device support html to view the receipt.',
            settings.EMAIL_HOST_USER,           # from email
            [email],                            # to email
            fail_silently=False,
            html_message=html_message
        )
        return redirect('adminTransactionsOverview')
    else:
        print('hhh')
        return redirect('adminTransactionsOverview')

