# django-gallery-core

Reusable Django primitives for ordered image galleries.

`django-gallery-core` is a small package for teams that want gallery behavior without pulling in a full CMS. It focuses on a narrow, stable API:

- an abstract ordered image model
- a migration-safe upload path helper
- a reusable DRF serializer base
- a reusable Django admin inline
- a service for syncing gallery uploads from multipart requests

## Why this package exists

Many Django projects need the same gallery pattern:
- a parent model such as `Project`, `CaseStudy`, or `BlogPost`
- a related ordered list of images
- admin editing support
- simple serializer output for public APIs
- safe upload handling for create and update flows

This package extracts that repeated plumbing into a reusable core while keeping app-specific decisions in your own code.

## Features

- `OrderedGalleryImage`: abstract base model for ordered image rows
- `GalleryUploadTo`: deconstructible upload helper compatible with Django migrations
- `build_gallery_upload_to(...)`: convenience factory for upload paths
- `OrderedGalleryImageSerializer`: serializer base for public API output
- `OrderedGalleryInline`: reusable Django admin inline
- `sync_gallery_uploads(...)`: service for adding and removing images during multipart form handling

## Installation

```bash
pip install django-gallery-core
```

For local development:

```bash
pip install -e ".[test]"
```

Add the app to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'gallery',
]
```

## Public API

The intended public surface area is:

- `gallery.models.OrderedGalleryImage`
- `gallery.models.GalleryUploadTo`
- `gallery.models.build_gallery_upload_to`
- `gallery.serializers.OrderedGalleryImageSerializer`
- `gallery.admin.OrderedGalleryInline`
- `gallery.services.sync_gallery_uploads`

Anything outside this surface should be treated as internal and may change more freely.

## Quick Start

### 1. Define a parent model and gallery image model

```python
from django.db import models
from gallery.models import OrderedGalleryImage, build_gallery_upload_to


class Project(models.Model):
    title = models.CharField(max_length=120)


class ProjectImage(OrderedGalleryImage):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='gallery_images',
    )
    image = models.ImageField(upload_to=build_gallery_upload_to('projects/gallery'))
```

### 2. Expose gallery data in an API serializer

```python
from rest_framework import serializers
from gallery.serializers import OrderedGalleryImageSerializer
from gallery.services import sync_gallery_uploads
from .models import Project, ProjectImage


class ProjectImageSerializer(OrderedGalleryImageSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'order']


class ProjectWriteSerializer(serializers.ModelSerializer):
    gallery = ProjectImageSerializer(source='gallery_images', many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'gallery']

    def update(self, instance, validated_data):
        request = self.context['request']
        # IDs to delete come from the client (e.g. a hidden field listing removed images)
        remove_ids = [int(x) for x in request.data.getlist('remove_gallery_ids') if x]
        instance = super().update(instance, validated_data)
        sync_gallery_uploads(
            instance=instance,
            related_name='gallery_images',
            image_model=ProjectImage,
            gallery_files=request.FILES.getlist('gallery_images'),
            remove_ids=remove_ids,
        )
        return instance
```

### 3. Reuse the admin inline

```python
from django.contrib import admin
from gallery.admin import OrderedGalleryInline
from .models import Project, ProjectImage


class ProjectImageInline(OrderedGalleryInline):
    model = ProjectImage


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
```

## Example

A minimal integration example lives in [example.py](./example.py).

## Design Goals

- Stay close to native Django and DRF patterns
- Keep the package small and readable
- Avoid forcing a full gallery domain model onto consuming apps
- Preserve migration safety for upload path helpers
- Support practical admin and API use cases first

## Non-Goals

- full media management
- asset optimization pipelines
- frontend gallery UI
- polymorphic attachment systems
- complete CMS abstractions

## Development

```bash
# Install all dev dependencies (tests + linting)
pip install -e ".[dev]"

# Run tests with coverage
pytest --cov=gallery --cov-report=term-missing

# Lint
ruff check .
```

## Versioning

This package is in early-stage development and currently targets a `0.x` release line. Expect additive improvements while the public API settles.

## License

MIT. See [LICENSE](./LICENSE).
