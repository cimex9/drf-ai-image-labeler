from config.settings.base import *

DEBUG = True

SECRET_KEY = os.environ.get("SECRET_KEY", "secret_key_local")
ALLOWED_HOSTS = ["*"]
