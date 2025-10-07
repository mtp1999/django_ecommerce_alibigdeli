from django.urls import path
from app_dashboard.customer_dashboard import views

app_name = 'customer'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('profile-delete-image/', views.ProfileDeleteImageView.as_view(), name='profile_delete_image'),
]
