from django.contrib import admin
from django.urls import path, include
from bills import views  # Import necessary views
from django.views.generic import TemplateView

urlpatterns = [
    # Custom admin login and dashboard
    path("custom_admin/login/", views.admin_login, name="admin_login"),
    path("custom_admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # User URLs
    path("user/login/", views.user_login, name="user_login"),
    path("user/dashboard/", views.user_dashboard, name="user_dashboard"),
    path("user/pay/", views.pay_bill, name="pay_bill"),
    path("user/download/", views.download_bill_pdf, name="download_bill_pdf"),

    # Home page
    path("", TemplateView.as_view(template_name="bills/home.html"), name="home"),

    # Built-in Django admin panel
    path("admin/", admin.site.urls),

    # Bills URLs (Ensure that delete_bill is included inside `bills/urls.py`)
    path("bills/", include("bills.urls")),
]
