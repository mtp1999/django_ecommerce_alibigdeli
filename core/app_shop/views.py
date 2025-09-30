import django.views.generic as cbv
from django.db.models import ExpressionWrapper, fields
from django.db.models import F
from app_shop.models import Product, ProductStatusType
from app_cart.cart import CartSession

class ProductGridView(cbv.ListView):
    template_name = 'app_shop/product_grid.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get query params except "page"
        params = self.request.GET.copy()
        if "page" in params:
            params.pop("page")
        context["querystring"] = params.urlencode()
        return context

    def get_paginate_by(self, queryset):
        """
        Override to allow ?per_page=... in the URL
        """
        per_page = self.request.GET.get("paginated_by")
        if per_page:
            try:
                return int(per_page)
            except ValueError:
                return self.paginate_by  # fallback if invalid
        return self.paginate_by

    def get_queryset(self):
        queryset = Product.objects.filter(status=ProductStatusType.publish.value).annotate(
            final_price=ExpressionWrapper(
                F('price') - ((F('price') * F('discount_percent')) / 100),
                output_field=fields.IntegerField()
            )
        )
        if title_q := self.request.GET.get('title_q'):
            queryset = queryset.filter(title__icontains=title_q)
        if product_category := self.request.GET.get('product_category'):
            queryset = queryset.filter(category__id=product_category)
        if min_price := self.request.GET.get('min_price'):
            queryset = queryset.filter(final_price__gte=min_price)
        if max_price := self.request.GET.get('max_price'):
            queryset = queryset.filter(final_price__lte=max_price)
        if order_by := self.request.GET.get('order_by'):
            queryset = queryset.order_by(order_by)

        return queryset


class ProductDetailView(cbv.DetailView):
    template_name = 'app_shop/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        context['check_product_in_cart'] = cart.check_product_in_cart(self.get_object().id)
        context['cart_item_quantity'] = cart.get_cart_item_quantity(self.get_object().id)
        return context

