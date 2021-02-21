from vough_backend.settings import BASE_DIR, INSTALLED_APPS, ROOT_URLCONF
from django.core.management.utils import get_random_secret_key

SECRET_KEY = get_random_secret_key()

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'settings/testdb.sqlite3',
    }
}