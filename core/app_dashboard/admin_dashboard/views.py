import django.views.generic as cbv
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import ExpressionWrapper, fields
from django.db.models import F
from app_account.models import Profile
from app_dashboard.utils import MessageMixin
from app_dashboard.permissions import HasAdminPermissionsMixin
from app_dashboard.admin_dashboard.forms import ProfileForm, ProductCreateForm, ProductEditForm
from app_shop.models import Product


class HomeView(HasAdminPermissionsMixin, LoginRequiredMixin, cbv.TemplateView):
    template_name = 'app_dashboard/admin/home.html'


class ChangePasswordView(HasAdminPermissionsMixin, MessageMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('app_dashboard:admin:change_password')
    template_name = 'app_dashboard/admin/change_password.html'
    success_message = 'رمز عبور با موفقیت تغییر یافت.'


class EditProfileView(HasAdminPermissionsMixin, MessageMixin, cbv.UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('app_dashboard:admin:edit_profile')
    template_name = 'app_dashboard/admin/edit_profile.html'
    success_message = 'پروفایل با موفقیت تغییر یافت.'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return redirect(reverse_lazy('app_dashboard:admin:edit_profile'))


class ProfileDeleteImageView(HasAdminPermissionsMixin, cbv.View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            profile.image = None
            profile.save()
        except:
            pass
        else:
            return JsonResponse({"message": 'ok'})


class ProductListView(HasAdminPermissionsMixin, cbv.ListView):
    template_name = 'app_dashboard/admin/product_list.html'
    paginate_by = 10

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
        queryset = Product.objects.all().annotate(
            final_price=ExpressionWrapper(
                F('price') - ((F('price') * F('discount_percent')) / 100),
                output_field=fields.IntegerField()
            )
        ).order_by('-id')
        if title_q := self.request.GET.get('title_q'):
            queryset = queryset.filter(title__icontains=title_q)
        if product_category := self.request.GET.get('product_category'):
            queryset = queryset.filter(category__id=product_category)
        if order_by := self.request.GET.get('order_by'):
            queryset = queryset.order_by(order_by)

        return queryset


class ProductCreateView(HasAdminPermissionsMixin, cbv.CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'app_dashboard/admin/product_create.html'

    def get_success_url(self):
        messages.success(self.request, 'محصول جدید با موفقیت ایجاد شد.')
        return reverse('app_dashboard:admin:product_list')

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return redirect(reverse_lazy('app_dashboard:admin:product_create'))


class ProductUpdateView(HasAdminPermissionsMixin, cbv.UpdateView):
    template_name = 'app_dashboard/admin/product_edit.html'
    model = Product
    form_class = ProductEditForm

    def get_success_url(self):
        messages.success(self.request, 'بروزرسانی با موفقیت انجام شد.')
        return reverse('app_dashboard:admin:product_edit', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return redirect(reverse_lazy('app_dashboard:admin:product_edit', kwargs={'pk': self.object.pk}))


class ProductDeleteView(HasAdminPermissionsMixin, cbv.DeleteView):
    template_name = 'app_dashboard/admin/product_delete.html'
    model = Product

    def get_success_url(self):
        messages.success(self.request, 'حذف محصول با موفقیت انجام شد.')
        return reverse('app_dashboard:admin:product_list')
