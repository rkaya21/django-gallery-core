from collections.abc import Iterable

__all__ = ['sync_gallery_uploads']

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
