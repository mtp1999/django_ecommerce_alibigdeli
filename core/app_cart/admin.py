from django.contrib import admin
from app_cart.models import Cart, CartItem


@admin.register(Cart)
class CustomCartAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
    )
    ordering = ("pk", "created_date")


@admin.register(CartItem)
class CustomCartItemAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "cart",
        "product",
        "quantity",
    )
    ordering = ("pk",)
