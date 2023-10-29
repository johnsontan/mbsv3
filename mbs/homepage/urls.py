from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('contact-us/submit', views.contactFormPost ,name="contactUsSubmit"),
    path('testpage/', views.testPage ,name="testPage"),
]