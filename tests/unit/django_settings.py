"""
This file acts as DJANGO_SETTINGS_MODULE for unit tests. This file is set as
Django settings file in the tests/unit/pytest.ini file.
"""
from django.core.management.utils import get_random_secret_key

from config.settings.base import *

DEBUG = False

SECRET_KEY = get_random_secret_key()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
