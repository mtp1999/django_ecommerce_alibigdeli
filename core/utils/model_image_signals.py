import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


def register_image_signals(model, field_name="image"):
    """
    Register simple image cleanup signals for any Django model.

    Automatically deletes the old image file when:
      - The model instance is deleted
      - The image field is replaced with a new one

    Args:
        model: Django model class (e.g. ProductImage)
        field_name (str): Name of the ImageField on the model
    """

    # --- DELETE signal ---
    @receiver(post_delete, sender=model)
    def auto_delete_file_on_delete(sender, instance, **kwargs):
        image_field = getattr(instance, field_name, None)
        if not image_field:
            return
        try:
            if hasattr(image_field, "path") and os.path.isfile(image_field.path):
                os.remove(image_field.path)
        except Exception:
            pass

    # --- CHANGE signal ---
    @receiver(pre_save, sender=model)
    def auto_delete_file_on_change(sender, instance, **kwargs):
        if not instance.pk:
            return
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            old_file = getattr(old_instance, field_name, None)
        except sender.DoesNotExist:
            return

        new_file = getattr(instance, field_name, None)

        try:
            if old_file and old_file != new_file:
                if hasattr(old_file, "path") and os.path.isfile(old_file.path):
                    os.remove(old_file.path)
        except Exception:
            pass
