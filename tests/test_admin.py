from gallery.admin import OrderedGalleryInline
from tests.models import AlbumImage


class TestOrderedGalleryInline:
    def test_is_tabular_inline(self):
        from django.contrib.admin import TabularInline
        assert issubclass(OrderedGalleryInline, TabularInline)

    def test_default_extra_is_zero(self):
        assert OrderedGalleryInline.extra == 0

    def test_can_subclass_with_model(self):
        class AlbumImageInline(OrderedGalleryInline):
            model = AlbumImage

        assert AlbumImageInline.extra == 0
