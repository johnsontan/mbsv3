from django.urls import path
from . import views

urlpatterns = [
    path('startpos/', views.startPos, name='startPos')

]