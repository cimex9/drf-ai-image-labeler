"""
This file contains non-django settings needed by the application itself.
Also, it contains the environment variables defined by the applications.

Requires that environment variables are only read from this file, never set or modified.
Default environment variable values are defined in `.default.env`.
"""

import os


# VLM-related
VLM_PROVIDER = os.getenv("VLM_PROVIDER", '')
VLM_MODEL = os.getenv("VLM_MODEL", '')
## Ollama VLM provider
OLLAMA_SERVER_URL = os.getenv("OLLAMA_SERVER_URL", '').rstrip('/')

# DB
PG_DB_HOST = os.getenv("PG_DB_HOST", '')
PG_DB_PORT = os.getenv("PG_DB_PORT", '')
PG_DB_NAME = os.getenv("PG_DB_NAME", '')
PG_DB_USER = os.getenv("PG_DB_USER", '')
PG_DB_PASSWORD = os.getenv("PG_DB_PASSWORD", '')

# Media
MINIO_URL = os.getenv("MINIO_URL", '')
MINIO_USERNAME = os.getenv("MINIO_USERNAME", '')
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD", '')
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", '')
