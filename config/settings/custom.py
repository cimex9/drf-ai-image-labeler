"""
This file contains non-django settings needed by the application itself.
Also, it contains the environment variables defined by the applications.

Requires that environment variables are only read from this file, never set or modified.
Default environment variable values are defined in `default.env`.
"""

import os


# AI
OLLAMA_SERVER_URL = os.environ["OLLAMA_SERVER_URL"].rstrip('/')

# DB
PG_DB_HOST = os.environ["PG_DB_HOST"]
PG_DB_PORT = os.environ["PG_DB_PORT"]
PG_DB_NAME = os.environ["PG_DB_NAME"]
PG_DB_USER = os.environ["PG_DB_USER"]
PG_DB_PASSWORD = os.environ["PG_DB_PASSWORD"]

# Media
MINIO_URL = os.environ["MINIO_URL"]
MINIO_USERNAME = os.environ["MINIO_USERNAME"]
MINIO_PASSWORD = os.environ["MINIO_PASSWORD"]
MINIO_BUCKET_NAME = os.environ["MINIO_BUCKET_NAME"]
