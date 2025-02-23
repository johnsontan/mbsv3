from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.employeeIndex, name="employeeIndex"),
    path('e-profile/', views.employeeProfile, name="employeeProfile"),
    path('employee-payslip-overview/', views.adminEmployeePayslipOverview, name="adminEmployeePayslipOverview"),
    path('insert-employee-payslip/', views.adminInsertEmployeePayslip, name="adminInsertEmployeePayslip"),
    path('delete-employee-payslip/<int:payslipID>', views.adminDeleteEmployeePayslip, name="adminEmployeePayslipDelete"),
    path('update-employee-payslip/<int:payslipID>', views.adminEditemployeePayslip, name="adminEmployeePayslipUpdate"),
    path('payslip/', views.employeePayslipOverview, name="employeePayslipOverview"),
    path('payslip/view/<int:id>', views.employeePayslipViewMore, name="employeePayslipViewMore"),
    path('admin-employees-leave-overview/', views.adminEmployeeLeaveOverview, name="adminEmployeeLeaveOverview"),
    path('admin-employees-leave-insert/', views.adminEmployeeLeaveInsert, name="adminEmployeeLeaveInsert"),
    path('admin-employees-leave-details/<int:pk>', views.adminEmployeeLeaveDetail, name="adminEmployeeLeaveDetail"),
    path('admin-employees-leave-approve/<int:pk>', views.adminApproveLeave, name="adminApproveLeave"),
    path('admin-employees-leave-reject/<int:pk>', views.adminRejectLeave, name="adminRejectLeave"),
    path('employee-apply-leave', views.employeeApplyLeave, name="employeeApplyLeave"),
    path('employee-leave-overview', views.employeeLeaveOverview, name="employeeLeaveOverview"),
    path('admin-add-frontend-employee-profile/', views.adminAddFrontendEmployee, name="adminAddFrontendEmployee"),
    path('admin-frontend-employee-profile-overview/', views.adminFrontendEmployeeProfileOverview, name="adminFrontendEmployeeProfileOverview"),
    path('admin-delete-frontend-employee-profile/<int:pk>', views.adminDeleteFrontendEmployeeProfile, name="adminDeleteFrontendEmployeeProfile"),
    path('admin-edit-frontend-employee-profile/<int:pk>', views.adminEditFrontendEmployeeProfile, name="adminEditFrontendEmployeeProfile"),
]