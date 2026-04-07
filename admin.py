from django.contrib import admin

__all__ = ['OrderedGalleryInline']


class OrderedGalleryInline(admin.TabularInline):
    extra: int = 0
