from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.adminCreateCustomer, name="adminCreateCustomer"),
    path('overview/', views.adminCustomerOverview, name="adminCustomerOverview"),
    path('userdetails/<int:pk>', views.adminCustomerDetails, name="adminUserDetails"),
    path('editUserDetails/<int:pk>', views.adminEditCustomerDetails, name="adminEditUserDetails"),
    path('deleteUserDetails/<int:pk>', views.adminDeleteCustomer, name="adminDeleteUserDetails"),
    path('voucher/', views.adminVoucherCustomer, name="adminVoucherCustomer"),
    path('credit/', views.adminCreditCustomer, name="adminCreditCustomer"),
    path('deleteNote/<int:pk>/<int:customerpk>', views.adminDeleteNote, name="adminDeleteNote"),
    path('issueVoucher/', views.adminIssueVoucherCustomer, name="adminIssueVoucherCustomer"),
    path('customerVoucherDetails/<int:pk>', views.adminCustomerVoucherDetail, name="adminCustomerVoucherDetail"),
    path('customerDeductVoucher/<int:pk>', views.adminDeductVoucher, name="adminDeductVoucher"),
    path('getCustomerProfile/', views.handle_customer_profile, name="handleCustomerProfile"),
]