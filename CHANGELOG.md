# Changelog

## Unreleased

- Removed `default_app_config` from `__init__.py` (deprecated since Django 3.2, no-op on Django 5+)
- `sync_gallery_uploads`: removed hardcoded `parent_field='project'` default; FK field is now auto-detected from `image_model` meta; explicit `parent_field` still accepted as an override
- Added standalone pytest-based test suite (`tests/`) with in-memory SQLite settings and self-contained test models; removed host-app-coupled `tests.py`
- Fixed CI workflow: now runs on the standalone repo root, installs `.[test]`, and executes `pytest` across Python 3.11 and 3.12

## 0.1.0

- Initial public package scaffold
- Added `OrderedGalleryImage` abstract base model
- Added `GalleryUploadTo` and `build_gallery_upload_to`
- Added `OrderedGalleryImageSerializer`
- Added `OrderedGalleryInline`
- Added `sync_gallery_uploads(...)`
- Added README and package metadata

