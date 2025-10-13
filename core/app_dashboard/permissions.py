from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from app_account.models import UserType


class HasAdminPermissionsMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        # called after LoginRequiredMixin ensures user is authenticated
        user = self.request.user
        return (
            user.is_active and
            getattr(user, "type", None) in (UserType.admin.value, UserType.superuser.value)
        )

    def handle_no_permission(self):
        # default: redirects to login if not authenticated; if authenticated but fails test_func,
        # it will call this method and by default redirects to login. You can override:
        if self.request.user.is_authenticated:
            # return a 403 instead of redirecting to login
            raise PermissionDenied("You don't have permission to view this page.")
        return super().handle_no_permission()


class HasCustomerPermissionsMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        # called after LoginRequiredMixin ensures user is authenticated
        user = self.request.user
        return (
            user.is_active and
            getattr(user, "type", None) == UserType.customer.value
        )

    def handle_no_permission(self):
        # default: redirects to login if not authenticated; if authenticated but fails test_func,
        # it will call this method and by default redirects to login. You can override:
        if self.request.user.is_authenticated:
            # return a 403 instead of redirecting to login
            raise PermissionDenied("You don't have permission to view this page.")
        return super().handle_no_permission()
