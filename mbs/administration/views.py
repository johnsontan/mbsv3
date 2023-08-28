from django.shortcuts import render

# Create your views here.

def adminIndex(request):
    return render(request, 'index.html')