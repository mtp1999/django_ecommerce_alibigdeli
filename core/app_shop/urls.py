from django.urls import path, re_path
from app_shop import views

app_name = 'app_shop'

urlpatterns = [
    path('product/list/grid/', views.ProductGridView.as_view(), name='product_grid'),
    # path('product/detail/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    re_path(r'^product/detail/(?P<slug>[-\w\u0600-\u06FF]+)/$', views.ProductDetailView.as_view(), name='product_detail'),
]
