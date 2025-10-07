from django.apps import AppConfig


class AppaccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_account"
    verbose_name = "app_account"

    def ready(self):
        # import here to avoid app registry issues
        from .models import Profile
        from utils.model_image_with_default_signals import register_image_with_default_signals

        # register signals for models
        register_image_with_default_signals(Profile, field_name="image")

