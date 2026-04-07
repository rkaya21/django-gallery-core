from django.db import models
from django.utils.deconstruct import deconstructible

__all__ = ['GalleryUploadTo', 'build_gallery_upload_to', 'OrderedGalleryImage']


@deconstructible
class GalleryUploadTo:
    """Migration-safe upload_to callable for gallery image fields.

    Stores the prefix as a plain string so Django's migration serializer
    can reconstruct the callable without pickling a lambda.

    Usage::

        image = models.ImageField(upload_to=GalleryUploadTo('projects/gallery'))
    """

    def __init__(self, prefix: str):
        self.prefix = prefix.strip('/ ')

    def __call__(self, instance, filename: str) -> str:
        return f'{self.prefix}/{filename}'


def build_gallery_upload_to(prefix: str) -> GalleryUploadTo:
    """Return a :class:`GalleryUploadTo` instance for the given prefix.

    Convenience factory so call sites read naturally::

        image = models.ImageField(upload_to=build_gallery_upload_to('projects/gallery'))
    """
    return GalleryUploadTo(prefix)


class OrderedGalleryImage(models.Model):
    """Abstract base model for an ordered gallery image row.

    Subclass this model, add a ForeignKey to the parent model, and override
    the ``image`` field with a project-specific ``upload_to`` path::

        class ProjectImage(OrderedGalleryImage):
            project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                        related_name='gallery_images')
            image = models.ImageField(upload_to=build_gallery_upload_to('projects/gallery'))

    Rows are ordered by ``order`` then ``id`` by default.
    """

    image = models.ImageField(upload_to='gallery/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['order', 'id']

    def get_image_url(self) -> str | None:
        """Return the URL of the image, or ``None`` if no image is set."""
        return self.image.url if self.image else None
