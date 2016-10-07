from .base import *  # noqa

from os import environ
from os import path

DEBUG = False
ALLOWED_HOSTS = environ.get('NABOJ_ZONA_ALLOWED_HOSTS').split()

BASE_DIR = BASE_DIR  # noqa
STATIC_ROOT = environ.get('NABOJ_ZONA_STATIC_ROOT')
MEDIA_ROOT = environ.get('NABOJ_ZONA_MEDIA_ROOT')
MEDIA_URL = 'media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environ.get('NABOJ_ZONA_DB_NAME'),
        'USER': environ.get('NABOJ_ZONA_DB_USER'),
        'PASSWORD': environ.get('NABOJ_ZONA_DB_PASSWD'),
        'HOST': environ.get('NABOJ_ZONA_DB_HOST', 'localhost'),
        'PORT': environ.get('NABOJ_ZONA_DB_PORT', ''),
    }
}
