from django.urls import path
from . import views


urlpatterns = [
    # Admin Routes
    path('custom_admin/login/', views.admin_login, name='admin_login'),
    path('custom_admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('custom_admin/add-bill/', views.add_bill, name='add_bill'),
    path('custom_admin/get-bills/', views.get_bills, name='get_bills'),  # ✅ Fixed issue here
    # path('custom_admin/delete-bill/<int:bill_id>/',views.delete_bill,name='delete_bill'),
    # path('custom_admin/delete-bill/<int:bill_id>/', views.delete_bill, name='delete_bill'),
     path('delete/<int:bill_id>/', views.delete_bill, name='delete_bill'),
    path('custom_admin/logout/', views.admin_logout, name='admin_logout'),

    # User Routes
    path('user/login/', views.user_login, name='user_login'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user/pay-bill/', views.pay_bill, name='pay_bill'),
    path('user/download-bill/', views.download_bill_pdf, name='download_bill_pdf'),
    path('user/logout/', views.user_logout, name='user_logout'),
    path('user/pay/', views.pay_bill, name='pay_bill'),


    # path('custom_admin/', include('bills.urls')),  # Make sure it’s included
]

