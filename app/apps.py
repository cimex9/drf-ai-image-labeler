import os

from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        if not os.environ.get('_APP_INIT_SCRIPTS') == '1':
            return

        from app.services.vlm_client_service import get_vlm_service
        get_vlm_service()
