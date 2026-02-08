import json
import logging
import boto3
from botocore.exceptions import ClientError
from django.conf import settings


logger = logging.getLogger(__name__)

class S3StorageService:
    def __init__(self):
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self.endpoint_url = settings.MINIO_URL
        self.access_key = settings.MINIO_USERNAME
        self.secret_key = settings.MINIO_PASSWORD

        self.client = boto3.client(
            's3',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            endpoint_url=self.endpoint_url,
        )

    def ensure_bucket_exists(self):
        """
        Ensure the bucket exists; create it if it doesn't.
        """
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
            logger.info(f"Bucket '{self.bucket_name}' already exists.")
        except ClientError as e:
            error_code = e.response['Error'].get('Code')
            if error_code in ['404', 'NoSuchBucket', None]:
                logger.info(f"Bucket '{self.bucket_name}' does not exist. Creating it...")
                try:
                    self.client.create_bucket(Bucket=self.bucket_name)
                    logger.info(f"Bucket '{self.bucket_name}' created successfully.")
                except ClientError as create_error:
                    logger.error(f"Failed to create bucket '{self.bucket_name}': {create_error}")
            else:
                logger.error(f"Error checking bucket '{self.bucket_name}': {e}")

    def ensure_public_read_policy(self):
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{self.bucket_name}/*"],
                }
            ],
        }

        try:
            self.client.put_bucket_policy(Bucket=self.bucket_name, Policy=json.dumps(policy))
            logger.info(
                "Public read policy ensured for bucket '%s'.",
                self.bucket_name,
            )
        except ClientError as e:
            logger.error(
                "Failed to set public policy for bucket '%s': %s",
                self.bucket_name,
                e,
            )
