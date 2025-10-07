import os
import logging
from typing import Optional

from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

logger = logging.getLogger(__name__)


def _get_field_default_name(field: models.Field) -> Optional[str]:
    """
    Return the default name for FileField/ImageField.
    Accepts string default or a callable default; if default is FieldFile-like, return .name.
    """
    default = field.get_default()
    # If callable default (rare), field.get_default() already called it.
    if hasattr(default, "name"):
        return default.name
    return default or None


def _delete_file_by_name(storage, name: str, fieldfile=None) -> None:
    """
    Delete a file using storage.delete if possible; fallback to removing local path.
    """
    try:
        if name and storage.exists(name):
            try:
                storage.delete(name)
                return
            except Exception:
                # fallthrough to local remove fallback
                pass
        # fallback: if fieldfile has .path and file exists locally
        if fieldfile is not None and hasattr(fieldfile, "path") and os.path.isfile(fieldfile.path):
            os.remove(fieldfile.path)
    except Exception as exc:
        logger.exception("Error deleting file %r: %s", name, exc)


def register_image_with_default_signals(model: models.Model, field_name: str = "image"):
    """
    Register pre_save and post_delete handlers for `model` and `field_name`.
    Call this once (e.g. in AppConfig.ready()) for each model you need.

    Example:
        register_image_signals(Profile, 'image')
        register_image_signals(User, 'avatar')
    """

    # Validate model has that field
    try:
        field = model._meta.get_field(field_name)
    except Exception as exc:
        raise ValueError(f"Model {model} has no field named '{field_name}'") from exc

    default_name = _get_field_default_name(field)

    # PRE_SAVE handler: replace cleared image with default and delete old non-default file
    def _pre_save(sender, instance, **kwargs):
        # only handle instances of the sender model
        if not isinstance(instance, sender):
            return

        # New instances: if no file provided, set to default
        if not instance.pk:
            new_ff = getattr(instance, field_name, None)
            new_name = getattr(new_ff, "name", None)
            if not new_name and default_name:
                # Set default on the field so DB saves the default path/name
                instance.__dict__.setdefault(field_name, None)
                # assign name directly (works with FieldFile API)
                setattr(instance, field_name, default_name)
            return

        # Existing instance: compare old and new by name
        try:
            old_inst = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            # nothing to do
            return

        old_ff = getattr(old_inst, field_name, None)
        new_ff = getattr(instance, field_name, None)

        old_name = getattr(old_ff, "name", None)
        new_name = getattr(new_ff, "name", None)

        # If new is empty -> set default
        if not new_name and default_name:
            setattr(instance, field_name, default_name)
            new_name = default_name

        # If nothing to delete or name unchanged, return
        if not old_name or old_name == new_name:
            return

        # don't delete default
        if default_name and old_name == default_name:
            return

        # try delete old file
        storage = getattr(old_ff, "storage", None)
        if storage:
            _delete_file_by_name(storage, old_name, fieldfile=old_ff)
        else:
            # fallback to path removal
            if hasattr(old_ff, "path") and os.path.isfile(old_ff.path):
                try:
                    os.remove(old_ff.path)
                except Exception:
                    logger.exception("Failed to remove old file at %s", old_ff.path)

    # POST_DELETE handler: delete file unless it's default
    def _post_delete(sender, instance, **kwargs):
        if not isinstance(instance, sender):
            return

        ff = getattr(instance, field_name, None)
        if not ff:
            return

        name = getattr(ff, "name", None)
        if not name:
            return

        if default_name and name == default_name:
            return

        storage = getattr(ff, "storage", None)
        if storage:
            _delete_file_by_name(storage, name, fieldfile=ff)
        else:
            if hasattr(ff, "path") and os.path.isfile(ff.path):
                try:
                    os.remove(ff.path)
                except Exception:
                    logger.exception("Failed to remove file at %s", ff.path)

    # Connect handlers with the specific sender
    pre_save.connect(_pre_save, sender=model, weak=False)
    post_delete.connect(_post_delete, sender=model, weak=False)

    # Return handlers if caller wants to keep references (e.g. for disconnect)
    return _pre_save, _post_delete
