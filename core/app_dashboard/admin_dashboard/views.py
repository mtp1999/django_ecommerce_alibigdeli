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
from app_dashboard.permissions import HasAdminPermissionsMixin
from app_dashboard.admin_dashboard.forms import ProfileForm


class HomeView(HasAdminPermissionsMixin, LoginRequiredMixin, cbv.TemplateView):
    template_name = 'app_dashboard/admin/home.html'


class ChangePasswordView(HasAdminPermissionsMixin, LoginRequiredMixin, MessageMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('app_dashboard:admin:change_password')
    template_name = 'app_dashboard/admin/change_password.html'
    success_message = 'رمز عبور با موفقیت تغییر یافت.'


class EditProfileView(HasAdminPermissionsMixin, LoginRequiredMixin, MessageMixin, cbv.UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('app_dashboard:admin:edit_profile')
    template_name = 'app_dashboard/admin/edit_profile.html'
    success_message = 'پروفایل با موفقیت تغییر یافت.'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return redirect(reverse_lazy('app_dashboard:admin:edit_profile'))


class ProfileDeleteImageView(HasAdminPermissionsMixin, LoginRequiredMixin, cbv.View):
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

