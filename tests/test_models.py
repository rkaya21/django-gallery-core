import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from gallery.models import GalleryUploadTo, OrderedGalleryImage
from tests.models import Album, AlbumImage


class TestGalleryUploadTo:
    def test_builds_expected_path(self):
        upload_to = GalleryUploadTo('projects/gallery')
        assert upload_to(None, 'shot.png') == 'projects/gallery/shot.png'

    def test_strips_leading_slash_from_prefix(self):
        upload_to = GalleryUploadTo('/projects/gallery')
        assert upload_to(None, 'shot.png') == 'projects/gallery/shot.png'

    def test_strips_trailing_slash_from_prefix(self):
        upload_to = GalleryUploadTo('projects/gallery/')
        assert upload_to(None, 'shot.png') == 'projects/gallery/shot.png'

    def test_strips_leading_and_trailing_slashes(self):
        upload_to = GalleryUploadTo('/projects/gallery/')
        assert upload_to(None, 'shot.png') == 'projects/gallery/shot.png'

    def test_deconstruct_roundtrip(self):
        original = GalleryUploadTo('projects/gallery')
        path, args, kwargs = original.deconstruct()
        reconstructed = GalleryUploadTo(*args, **kwargs)
        assert reconstructed(None, 'shot.png') == original(None, 'shot.png')

    def test_build_gallery_upload_to_factory(self):
        from gallery.models import build_gallery_upload_to
        upload_to = build_gallery_upload_to('albums/gallery')
        assert isinstance(upload_to, GalleryUploadTo)
        assert upload_to(None, 'cover.png') == 'albums/gallery/cover.png'


class TestOrderedGalleryImageMeta:
    def test_is_abstract(self):
        assert OrderedGalleryImage._meta.abstract is True

    def test_default_ordering(self):
        assert list(OrderedGalleryImage._meta.ordering) == ['order', 'id']


@pytest.mark.django_db
class TestGetImageUrl:
    def test_returns_url_when_image_set(self):
        album = Album.objects.create(title='Test')
        img = AlbumImage.objects.create(
            album=album,
            image=SimpleUploadedFile('photo.png', b'data', content_type='image/png'),
            order=1,
        )
        assert img.get_image_url() is not None
        assert 'photo.png' in img.get_image_url()

    def test_returns_none_when_image_empty(self):
        album = Album.objects.create(title='Test')
        img = AlbumImage.objects.create(album=album, image=None, order=1)
        assert img.get_image_url() is None
