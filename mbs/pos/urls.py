from django.urls import path
from . import views

urlpatterns = [
    path('startpos/', views.startPos, name='startPos'),
    path('transaction-overview/', views.adminTransactionsOverview, name='adminTransactionsOverview'),
    path('transaction-details/<int:pk>', views.adminViewTransactionDetails, name='adminViewTransactionDetails'),
    path('edit-transaction/<int:pk>', views.adminEditTransaction, name='adminEditTransaction'),
    path('receipt/<int:pk>', views.generateTransactionReceipt, name='generateTransactionReceipt'),
    path('email-receipt/', views.send_email_receipt, name='sendEmailReceipt'),
]