from django.shortcuts import render, redirect
from .models import SalesTransaction, SaleServices, ServiceImages
from .forms import SalesTransactionForm, SaleServiceFormset, ServiceImageFormset

# Create your views here.

def startPos(request):
    if request.method == 'POST':
        form = SalesTransactionForm(request.POST)
        #1. Save the sales transaction
        if form.is_valid():
            sales_transaction = form.save()
            sale_service_formset = SaleServiceFormset(request.POST, instance=sales_transaction)
            #2. Save the sale service and set the FK to sales transaction
            if sale_service_formset.is_valid():
                sale_services = sale_service_formset.save()

                # For each SaleService, process the ServiceImages formset
                for sale_service in sale_services:
                    service_image_formset = ServiceImageFormset(request.POST, instance=sale_service)
                    if service_image_formset.is_valid():
                        service_image_formset.save()
            return redirect('pos-startpos.html')  # Replace with your view name or URL
    else:
        form = SalesTransactionForm()
        sale_service_formset = SaleServiceFormset(queryset=SaleServices.objects.none())
        service_image_formset = ServiceImageFormset(queryset=ServiceImages.objects.none())
    return render(request, 'pos-startpos.html', {'form': form, 'sale_service_formset': sale_service_formset, 'service_image_formset': service_image_formset})


