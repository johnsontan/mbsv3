from django.urls import path, include
from . import views
from employee.views import adminEmployeeOverview, adminEmployeeEditProfile
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('pos.urls')),
    path('employee/', include('employee.urls')),
    path('customer/', include('customer.urls')),
    path('index/', views.adminIndex, name='adminIndex'),
    path('register/', views.adminRegister, name='registration'),
    path('login/', views.adminLogin, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.adminProfile, name='adminProfile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('employee-overview/', adminEmployeeOverview, name='adminEmployeeOverview'),
    path('employee-edit/<int:id>', adminEmployeeEditProfile, name='adminEmployeeEditProfile'),
    path('productOverview/', views.adminProductOverview, name='adminProductOverview'),
    path('registerProduct/', views.adminProductRegister, name='adminProductRegister'),
    path('deleteProduct/<int:pk>', views.adminDeleteProduct, name='adminDeleteProduct'),
    path('productDetails/<int:pk>', views.adminProductDetails, name='adminProductDetails'),
    path('productEdit/<int:pk>', views.adminEditProduct, name='adminEditProduct'),
    path('feedback-overview/', views.adminFeedbackOverview, name='adminFeedbackOverview'),
    path('feedback-delete/<int:pk>', views.adminFeedbackDelete, name='adminFeedbackDelete'),
    path('registerFrontendBanner/', views.adminAddFrontendBanner, name='adminAddFrontendBanner'),
    path('frontendBannerOverview/', views.adminFrontendBannerOverview, name='adminFrontendBannerOverview'),
    path('fronendSelect/', views.handle_frontend_select, name='handleFrontendSelect'),
    path('editFrontendBanner/<int:pk> ', views.adminEditFrontendBanner, name='adminEditFrontendBanner'),
    path('deleteFrontendBanner/<int:pk> ', views.adminDeleteFrontendBanner, name='adminDeleteFrontendBanner'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)