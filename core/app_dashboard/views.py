import django.views.generic as cbv
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from app_account.models import UserType


class DashboardView(LoginRequiredMixin, cbv.View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active:
            if request.user.type == UserType.customer.value:
                return redirect(reverse_lazy('app_dashboard:customer:home'))
            elif request.user.type in (UserType.admin.value, UserType.superuser.value):
                return redirect(reverse_lazy('app_dashboard:admin:home'))
        else:
            return redirect(reverse_lazy('app_account:login'))
        return super().dispatch(request, *args, **kwargs)
