from django.urls import path, include
from app_dashboard import views

app_name = 'app_dashboard'

urlpatterns = [
    path('home/', views.DashboardView.as_view(), name='home'),
    path('admin/', include('app_dashboard.admin_dashboard.urls')),
    path('customer/', include('app_dashboard.customer_dashboard.urls')),
]
