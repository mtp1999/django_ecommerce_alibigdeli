from django import template
from app_shop.models import ProductCategory, Product, ProductStatusType
from django.db.models import ExpressionWrapper, fields
from django.db.models import F

register = template.Library()


@register.simple_tag
def product_categories():
    categories = ProductCategory.objects.all()
    return categories


@register.inclusion_tag('includes/latest_products.html')
def latest_products():
    products = Product.objects.filter(status=ProductStatusType.publish.value).order_by('-created_date')[:8].annotate(
        final_price=ExpressionWrapper(
            F('price') - ((F('price') * F('discount_percent')) / 100),
            output_field=fields.IntegerField()
        )
    )
    return {'products': products}


@register.inclusion_tag('includes/similar_products.html')
def similar_products(product):
    categories = product.category.all()
    products = Product.objects.filter(status=ProductStatusType.publish.value, category__in=categories).order_by('-created_date')[:4].annotate(
        final_price=ExpressionWrapper(
            F('price') - ((F('price') * F('discount_percent')) / 100),
            output_field=fields.IntegerField()
        )
    )
    return {'products': products}