from django.core.exceptions import PermissionDenied
from app_account.models import UserType


class HasAdminPermissionsMixin:

    def has_permission(self, request, *args, **kwargs):
        return bool(request.user.type in (UserType.admin.value, UserType.superuser.value)) and bool(request.user.is_active)

    def handle_no_permission(self, request, *args, **kwargs):
        # either raise PermissionDenied or return HttpResponseForbidden
        # Raising PermissionDenied will be handled by Django and can use custom 403 page.
        raise PermissionDenied()

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission(request, *args, **kwargs):
            return self.handle_no_permission(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class HasCustomerPermissionsMixin:

    def has_permission(self, request, *args, **kwargs):
        return bool(request.user.type == UserType.customer.value) and bool(request.user.is_active)

    def handle_no_permission(self, request, *args, **kwargs):
        # either raise PermissionDenied or return HttpResponseForbidden
        # Raising PermissionDenied will be handled by Django and can use custom 403 page.
        raise PermissionDenied()

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission(request, *args, **kwargs):
            return self.handle_no_permission(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)