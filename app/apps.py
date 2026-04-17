from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        from app.services.vlm_client_service import get_vlm_service

        get_vlm_service()
