from django.db import models
from django.utils.deconstruct import deconstructible

__all__ = ['GalleryUploadTo', 'build_gallery_upload_to', 'OrderedGalleryImage']


@deconstructible
class GalleryUploadTo:
    def __init__(self, prefix: str):
        self.prefix = prefix.strip('/ ')

    def __call__(self, instance, filename: str) -> str:
        return f'{self.prefix}/{filename}'


def build_gallery_upload_to(prefix: str):
    return GalleryUploadTo(prefix)


class OrderedGalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['order', 'id']
