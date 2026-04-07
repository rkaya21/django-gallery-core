from rest_framework import serializers

__all__ = ['OrderedGalleryImageSerializer']


class OrderedGalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'image', 'order']

    def get_image(self, obj):
        return obj.image.url if obj.image else None

