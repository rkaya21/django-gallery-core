from django.db import models

from gallery.models import OrderedGalleryImage, build_gallery_upload_to


class ExampleProject(models.Model):
    title = models.CharField(max_length=120)


class ExampleProjectImage(OrderedGalleryImage):
    project = models.ForeignKey(
        ExampleProject,
        on_delete=models.CASCADE,
        related_name='gallery_images',
    )
    image = models.ImageField(upload_to=build_gallery_upload_to('projects/gallery'))

