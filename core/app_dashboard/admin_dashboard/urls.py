from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app_dashboard.admin_dashboard import views

app_name = 'admin'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('profile-delete-image/', views.ProfileDeleteImageView.as_view(), name='profile_delete_image'),
    path('products/list/', views.ProductListView.as_view(), name='product_list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/edit/<int:pk>/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
