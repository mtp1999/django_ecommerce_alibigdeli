from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from app_shop import views

app_name = 'app_shop'

urlpatterns = [
    path('product/list/grid/', views.ProductGridView.as_view(), name='product_grid'),
    # path('product/detail/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    re_path(r'^product/detail/(?P<slug>[-\w\u0600-\u06FF]+)/$', views.ProductDetailView.as_view(), name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
