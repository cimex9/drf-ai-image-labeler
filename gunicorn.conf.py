import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
os.environ["_APP_INIT_SCRIPTS"] = '1'
