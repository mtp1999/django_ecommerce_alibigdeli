import django.views.generic as cbv
from django.http import JsonResponse
from django.shortcuts import redirect
from app_cart.cart import CartSession


class SessionAddProductView(cbv.View):
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        if pid := request.POST.get('product_id'):
            cart.add_product(pid)
        return JsonResponse({'cart': cart.get_cart_items(), 'quantity': cart.get_cart_total_quantity()})


class SessionRemoveProductView(cbv.View):
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        if pid := request.POST.get('product_id'):
            cart.remove_product(pid)
        return JsonResponse({'cart': cart.get_cart_items()})


class SessionChangeProductQuantityView(cbv.View):
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        try:
            pid = request.POST.get('product_id')
            quantity = request.POST.get('quantity')
            cart.change_product_quantity(pid, quantity)
            return JsonResponse({'cart': cart.get_cart_items()})
        except:
            return redirect(request.path)


class SessionCartSummaryView(cbv.TemplateView):
    template_name = 'app_cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        context['cart_details'] = cart.get_cart_details(with_products=True)
        print(context['cart_details'])
        return context

