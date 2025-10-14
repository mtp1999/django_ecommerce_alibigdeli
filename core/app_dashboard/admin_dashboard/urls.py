from django.urls import path
from app_dashboard.admin_dashboard import views

app_name = 'admin'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('profile-delete-image/', views.ProfileDeleteImageView.as_view(), name='profile_delete_image'),
    path('products/list/', views.ProductListView.as_view(), name='product_list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/pid-<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/pid-<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('products/pid-<int:pk>/images/', views.ProductImageListView.as_view(), name='product_images'),
    path('products/img-id-<int:pk>/delete/', views.ProductImageDeleteView.as_view(), name='product_images_delete'),
]
