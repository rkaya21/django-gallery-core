from django.db import models

from gallery.models import OrderedGalleryImage, build_gallery_upload_to


class Album(models.Model):
    title = models.CharField(max_length=120)

    class Meta:
        app_label = 'tests'


class AlbumImage(OrderedGalleryImage):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='gallery_images',
    )
    image = models.ImageField(upload_to=build_gallery_upload_to('albums/gallery'))

    class Meta(OrderedGalleryImage.Meta):
        app_label = 'tests'
