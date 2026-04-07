import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

from gallery.services import reorder_gallery, sync_gallery_uploads
from tests.models import Album, AlbumImage


def make_image(name='test.png'):
    return SimpleUploadedFile(name, b'image-data', content_type='image/png')


@pytest.mark.django_db
class TestSyncGalleryUploads:
    def test_creates_images_in_order(self):
        album = Album.objects.create(title='Test Album')

        sync_gallery_uploads(
            instance=album,
            related_name='gallery_images',
            image_model=AlbumImage,
            gallery_files=[make_image('a.png'), make_image('b.png')],
        )

        orders = list(album.gallery_images.values_list('order', flat=True))
        assert orders == [1, 2]

    def test_order_appends_after_existing_images(self):
        album = Album.objects.create(title='Test Album')
        AlbumImage.objects.create(album=album, image=make_image('existing.png'), order=1)

        sync_gallery_uploads(
            instance=album,
            related_name='gallery_images',
            image_model=AlbumImage,
            gallery_files=[make_image('new.png')],
        )

        orders = list(album.gallery_images.order_by('order').values_list('order', flat=True))
        assert orders == [1, 2]

    def test_removes_requested_ids(self):
        album = Album.objects.create(title='Test Album')
        img = AlbumImage.objects.create(album=album, image=make_image('del.png'), order=1)

        sync_gallery_uploads(
            instance=album,
            related_name='gallery_images',
            image_model=AlbumImage,
            gallery_files=[],
            remove_ids=[img.id],
        )

        assert not album.gallery_images.exists()

    def test_empty_and_none_files_are_skipped(self):
        album = Album.objects.create(title='Test Album')

        sync_gallery_uploads(
            instance=album,
            related_name='gallery_images',
            image_model=AlbumImage,
            gallery_files=[None, ''],
        )

        assert album.gallery_images.count() == 0

    def test_remove_then_add_in_single_call(self):
        album = Album.objects.create(title='Test Album')
        img = AlbumImage.objects.create(album=album, image=make_image('old.png'), order=1)

        sync_gallery_uploads(
            instance=album,
            related_name='gallery_images',
            image_model=AlbumImage,
            gallery_files=[make_image('new.png')],
            remove_ids=[img.id],
        )

        assert album.gallery_images.count() == 1
        assert album.gallery_images.first().order == 1

    def test_remove_ids_none_does_not_error(self):
        album = Album.objects.create(title='Test Album')

        sync_gallery_uploads(
            instance=album,
            related_name='gallery_images',
            image_model=AlbumImage,
            gallery_files=[make_image('a.png')],
            remove_ids=None,
        )

        assert album.gallery_images.count() == 1

    def test_explicit_parent_field_overrides_auto_detection(self):
        album = Album.objects.create(title='Test Album')

        sync_gallery_uploads(
            instance=album,
            related_name='gallery_images',
            image_model=AlbumImage,
            gallery_files=[make_image('a.png')],
            parent_field='album',
        )

        assert album.gallery_images.count() == 1


@pytest.mark.django_db
class TestReorderGallery:
    def test_reorders_images(self):
        album = Album.objects.create(title='Test')
        img1 = AlbumImage.objects.create(album=album, image=make_image('a.png'), order=1)
        img2 = AlbumImage.objects.create(album=album, image=make_image('b.png'), order=2)
        img3 = AlbumImage.objects.create(album=album, image=make_image('c.png'), order=3)

        reorder_gallery(
            instance=album,
            related_name='gallery_images',
            new_order=[img3.id, img1.id, img2.id],
        )

        assert AlbumImage.objects.get(id=img3.id).order == 1
        assert AlbumImage.objects.get(id=img1.id).order == 2
        assert AlbumImage.objects.get(id=img2.id).order == 3

    def test_raises_on_mismatched_ids(self):
        album = Album.objects.create(title='Test')
        AlbumImage.objects.create(album=album, image=make_image('a.png'), order=1)

        with pytest.raises(ValueError, match='new_order must contain exactly the same IDs'):
            reorder_gallery(
                instance=album,
                related_name='gallery_images',
                new_order=[9999],
            )

    def test_raises_on_missing_ids(self):
        album = Album.objects.create(title='Test')
        img1 = AlbumImage.objects.create(album=album, image=make_image('a.png'), order=1)
        img2 = AlbumImage.objects.create(album=album, image=make_image('b.png'), order=2)

        with pytest.raises(ValueError):
            reorder_gallery(
                instance=album,
                related_name='gallery_images',
                new_order=[img1.id],  # img2 eksik
            )

    def test_raises_on_extra_ids(self):
        album = Album.objects.create(title='Test')
        img1 = AlbumImage.objects.create(album=album, image=make_image('a.png'), order=1)

        with pytest.raises(ValueError):
            reorder_gallery(
                instance=album,
                related_name='gallery_images',
                new_order=[img1.id, 9999],  # fazladan ID
            )


class TestResolveParentField:
    def test_raises_when_no_fk_found(self):
        class OrphanModel(models.Model):
            name = models.CharField(max_length=10)

            class Meta:
                app_label = 'tests'

        album = Album.__new__(Album)

        with pytest.raises(ValueError, match='OrphanModel'):
            sync_gallery_uploads(
                instance=album,
                related_name='gallery_images',
                image_model=OrphanModel,
                gallery_files=[],
            )
