from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'user', 'get_decoded', 'expire_date')
    ordering = ('-expire_date',)
    readonly_fields = ('user', 'get_decoded')

    def user(self, obj):
        data = obj.get_decoded()
        user_id = data.get('_auth_user_id')
        if user_id:
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return "Unknown"
        return "Anonymous"

    user.short_description = "User"

    def get_decoded(self, obj):
        return obj.get_decoded()
    get_decoded.short_description = "Data"


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "id",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "is_verified",
        "created_date",
    )
    list_display_links = (
        "id",
        "email",
    )
    list_filter = ("email", "is_staff", "is_active", "is_superuser", "is_verified")
    fieldsets = (
        ("Basic Information", {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                    "type",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("created_date", "updated_date", "last_login")}),
    )
    readonly_fields = ("created_date", "updated_date", "last_login")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email", "is_staff", "is_active", "is_superuser", "is_verified")
    ordering = (
        "pk",
        "email",
    )


class CustomProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = (
        "pk",
        "user",
        "first_name",
        "last_name",
        "phone_number",
    )
    ordering = ("pk",)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, CustomProfileAdmin)
