from rest_framework import serializers

__all__ = ['OrderedGalleryImageSerializer']


class OrderedGalleryImageSerializer(serializers.ModelSerializer):
    """Read-only serializer base for ordered gallery image rows.

    Subclass this and set ``Meta.model`` and ``Meta.fields``::

        class ProjectImageSerializer(OrderedGalleryImageSerializer):
            class Meta(OrderedGalleryImageSerializer.Meta):
                model = ProjectImage
                fields = ['id', 'image', 'order']

    The ``image`` field returns the absolute URL of the file via
    :meth:`get_image`, or ``None`` if no file is stored.
    """

    image = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'image', 'order']

    def get_image(self, obj) -> str | None:
        """Return the image URL, or ``None`` if no image is set."""
        return obj.image.url if obj.image else None
