from django.core.management.base import BaseCommand

from app.services import S3StorageService


class Command(BaseCommand):
    help = "Initialize MinIO bucket and policies. Idempotent action."

    def handle(self, *args, **options):
        storage_service = S3StorageService()
        storage_service.ensure_bucket_exists()
        storage_service.ensure_public_read_policy()
        self.stdout.write(self.style.SUCCESS("S3 storage initialized."))
