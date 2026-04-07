from collections.abc import Iterable

__all__ = ['sync_gallery_uploads', 'reorder_gallery']

from django.core.files.uploadedfile import UploadedFile
from django.db.models import ForeignKey, Model


def _resolve_parent_field(image_model: type[Model], instance: Model) -> str:
    parent_class = type(instance)
    for field in image_model._meta.get_fields():
        if isinstance(field, ForeignKey) and issubclass(parent_class, field.related_model):
            return field.name
    raise ValueError(
        f"Could not find a ForeignKey on {image_model.__name__} pointing to "
        f"{parent_class.__name__}. Pass parent_field explicitly."
    )


def sync_gallery_uploads(
    *,
    instance: Model,
    related_name: str,
    image_model: type[Model],
    gallery_files: Iterable[UploadedFile | None],
    remove_ids: list[int] | None = None,
    parent_field: str | None = None,
) -> None:
    """Add new gallery images and optionally remove existing ones.

    Intended for use inside form or serializer save methods that handle
    multipart file uploads.

    :param instance: The parent model instance owning the gallery.
    :param related_name: The reverse relation name on ``instance``
        (e.g. ``'gallery_images'``).
    :param image_model: The concrete image model class to create rows in.
    :param gallery_files: Iterable of uploaded files. ``None`` and falsy
        values are silently skipped.
    :param remove_ids: Primary keys of existing image rows to delete before
        adding new ones. Pass ``None`` or an empty list to skip deletion.
    :param parent_field: Name of the ForeignKey field on ``image_model``
        pointing to the parent. Detected automatically when omitted.
    """
    if parent_field is None:
        parent_field = _resolve_parent_field(image_model, instance)

    manager = getattr(instance, related_name)

    if remove_ids:
        manager.filter(id__in=remove_ids).delete()

    files = [image_file for image_file in gallery_files if image_file]
    if not files:
        return

    next_order = manager.count()
    for offset, image_file in enumerate(files, start=1):
        image_model.objects.create(**{
            parent_field: instance,
            'image': image_file,
            'order': next_order + offset,
        })


def reorder_gallery(
    *,
    instance: Model,
    related_name: str,
    new_order: list[int],
) -> None:
    """Reorder gallery images by assigning new ``order`` values.

    :param instance: The parent model instance owning the gallery.
    :param related_name: The reverse relation name on ``instance``
        (e.g. ``'gallery_images'``).
    :param new_order: List of image primary keys in the desired display order.
        Must contain exactly the same IDs as the current gallery — no more,
        no fewer.
    :raises ValueError: If ``new_order`` does not match the current set of IDs.
    """
    manager = getattr(instance, related_name)
    existing_ids = set(manager.values_list('id', flat=True))

    if set(new_order) != existing_ids:
        raise ValueError(
            f"new_order must contain exactly the same IDs as the current gallery. "
            f"Expected {sorted(existing_ids)}, got {sorted(new_order)}."
        )

    for position, image_id in enumerate(new_order, start=1):
        manager.filter(id=image_id).update(order=position)
