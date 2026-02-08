from django.apps import AppConfig

from app.services import S3StorageService


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        # init the minio bucket and bucket public read settings on app startup
        storage_service = S3StorageService()
        storage_service.ensure_bucket_exists()
        storage_service.ensure_public_read_policy()
