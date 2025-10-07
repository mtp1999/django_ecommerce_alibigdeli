from django.apps import AppConfig


class AppShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_shop'

    def ready(self):
        # import here to avoid app registry issues
        from .models import Product, ProductImage
        from utils.model_image_with_default_signals import register_image_with_default_signals
        from utils.model_image_signals import register_image_signals

        # register signals for models
        register_image_with_default_signals(Product, field_name="image")
        register_image_signals(ProductImage, field_name="image")

