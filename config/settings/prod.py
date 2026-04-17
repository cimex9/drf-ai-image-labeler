import os

from config.settings.base import *


DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(',')

