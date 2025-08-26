from django.contrib import admin
from app_website.models import Contact, Newsletter


@admin.register(Contact)
class CustomContactAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "email",
        "full_name",
        "status",
        "created_date"
    )
    list_filter = (
        "email",
        "status",
        "phone"
    )


@admin.register(Newsletter)
class CustomNewsletterAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "email",
        "is_active",
        "created_date"
    )
    list_filter = (
        "email",
        "is_active",
    )
