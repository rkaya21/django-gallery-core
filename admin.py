from django.contrib import admin

__all__ = ['OrderedGalleryInline']


class OrderedGalleryInline(admin.TabularInline):
    """Reusable tabular inline for ordered gallery images.

    Subclass this and set ``model`` to the concrete image model::

        class ProjectImageInline(OrderedGalleryInline):
            model = ProjectImage

        @admin.register(Project)
        class ProjectAdmin(admin.ModelAdmin):
            inlines = [ProjectImageInline]
    """

    extra: int = 0
