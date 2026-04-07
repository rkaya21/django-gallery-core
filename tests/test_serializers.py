import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from gallery.serializers import OrderedGalleryImageSerializer
from tests.models import Album, AlbumImage


class AlbumImageSerializer(OrderedGalleryImageSerializer):
    class Meta(OrderedGalleryImageSerializer.Meta):
        model = AlbumImage
        fields = ['id', 'image', 'order']


@pytest.mark.django_db
class TestOrderedGalleryImageSerializer:
    def test_exposes_image_url(self):
        album = Album.objects.create(title='Test')
        img = AlbumImage.objects.create(
            album=album,
            image=SimpleUploadedFile('cover.png', b'image-data', content_type='image/png'),
            order=1,
        )

        data = AlbumImageSerializer(img).data

        assert data['image'] is not None
        assert 'cover.png' in data['image']

    def test_exposes_order_field(self):
        album = Album.objects.create(title='Test')
        img = AlbumImage.objects.create(
            album=album,
            image=SimpleUploadedFile('shot.png', b'image-data', content_type='image/png'),
            order=3,
        )

        data = AlbumImageSerializer(img).data

        assert data['order'] == 3

    def test_exposes_id_field(self):
        album = Album.objects.create(title='Test')
        img = AlbumImage.objects.create(
            album=album,
            image=SimpleUploadedFile('shot.png', b'image-data', content_type='image/png'),
            order=1,
        )

        data = AlbumImageSerializer(img).data

        assert data['id'] == img.id


class TestGetImageMethod:
    def test_returns_none_when_image_is_falsy(self):
        class FakeObj:
            image = None

        serializer = AlbumImageSerializer()
        assert serializer.get_image(FakeObj()) is None
