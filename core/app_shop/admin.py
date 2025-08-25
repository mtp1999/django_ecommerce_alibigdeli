from django.contrib import admin
from app_shop.models import Product, ProductCategory, ProductImage


@admin.register(Product)
class CustomProductAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "slug",
        "get_categories",
        "stock",
        "price",
        "discount_percent",
        "get_price",
        "status"
    )
    ordering = ("pk",)

    def get_categories(self, obj):
        return ", ".join([cat.title for cat in obj.category.all()])

    get_categories.short_description = "Categories"


@admin.register(ProductCategory)
class CustomProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "slug",
        "created_date"
    )
    ordering = ("pk",)


@admin.register(ProductImage)
class CustomProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "product",
    )
    ordering = ("pk",)
