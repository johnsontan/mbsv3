from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages
from django.urls import reverse
from administration.models import FrontendBanner
from employee.models import EmployeeFrontendProfile


# Create your views here.

def homepage(request):
    form = ContactForm()

    #get all the banners
    banners = FrontendBanner.objects.filter(selected=1).order_by('-created_at')

    #get all team members
    members = EmployeeFrontendProfile.objects.all()
    
    context = {
        'form' : form,
        'banners':banners,
        'members' : members
    }
    return render(request, 'homeindex.html', context)

def contactFormPost(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us, we will get back to your in 48 business hours.')
            return redirect(reverse('homepage')+ '#contact')
        else:
            messages.success(request, 'Error in submitting the form.')
            return redirect(reverse('homepage')+ '#contact')
            
def testPage(request):
    return render(request, 'hair_botox_repair.html')