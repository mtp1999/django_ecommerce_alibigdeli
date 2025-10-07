import django.views.generic as cbv
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from app_account.models import Profile
from app_dashboard.utils import MessageMixin
from app_dashboard.permissions import HasCustomerPermissionsMixin
from app_dashboard.customer_dashboard.forms import ProfileForm


class HomeView(HasCustomerPermissionsMixin, LoginRequiredMixin, cbv.TemplateView):
    template_name = 'app_dashboard/customer/home.html'


class ChangePasswordView(HasCustomerPermissionsMixin, LoginRequiredMixin, MessageMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('app_dashboard:customer:change_password')
    template_name = 'app_dashboard/customer/change_password.html'
    success_message = 'رمز عبور با موفقیت تغییر یافت.'


class EditProfileView(HasCustomerPermissionsMixin, LoginRequiredMixin, MessageMixin, cbv.UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('app_dashboard:customer:edit_profile')
    template_name = 'app_dashboard/customer/edit_profile.html'
    success_message = 'پروفایل با موفقیت تغییر یافت.'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return redirect(reverse_lazy('app_dashboard:customer:edit_profile'))


class ProfileDeleteImageView(HasCustomerPermissionsMixin, LoginRequiredMixin, cbv.View):
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

