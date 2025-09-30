from django.urls import path
from app_cart import views

app_name = 'app_cart'

urlpatterns = [
    path('session/add-product/', views.SessionAddProductView.as_view(), name='session_add_product'),
    path('session/remove-product/', views.SessionRemoveProductView.as_view(), name='session_remove_product'),
    path('session/change-product-quantity/', views.SessionChangeProductQuantityView.as_view(), name='session_change_product_quantity'),
    path('session/cart/summary/', views.SessionCartSummaryView.as_view(), name='session_cart_summary'),
]
