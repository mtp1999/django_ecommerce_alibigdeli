from django.apps import AppConfig


class AppCartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_cart'

    def ready(self):
        import app_cart.signals
        return super().ready()
