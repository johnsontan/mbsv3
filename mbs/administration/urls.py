from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('pos.urls')),
    path('index/', views.adminIndex, name='registration')

]
