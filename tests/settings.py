import tempfile

SECRET_KEY = 'test-secret-key-not-for-production'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'gallery',
    'tests',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = tempfile.mkdtemp()
MEDIA_URL = '/media/'

USE_TZ = True
