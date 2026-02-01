from __future__ import annotations

"""Utilities for uploading and downloading PDF files in GCP Cloud Storage."""

from dataclasses import dataclass
from io import BytesIO
from typing import Optional

from google.cloud import storage

from .configs import *

@dataclass(frozen=True)
class GCPStorageConfig:
    """Configuration for connecting to a GCP Storage bucket."""
    bucket_name: str
    credentials_json: Optional[str] = None
    project_id: Optional[str] = None

def get_storage_client(config: Optional[GCPStorageConfig] = None) -> storage.Client:
    """
    Build a GCP Storage client.

    Uses explicit service-account JSON if provided; otherwise relies on
    Application Default Credentials (ADC) in the runtime environment.
    This function does not validate bucket access; it only creates a client.
    """
    if config is None:
        config = GCPStorageConfig(
            bucket_name=DEFAULT_GCP_BUCKET,
            credentials_json=DEFAULT_GCP_CREDENTIALS_JSON,
            project_id=DEFAULT_GCP_PROJECT_ID,
        )

    if config.credentials_json:
        return storage.Client.from_service_account_json(
            config.credentials_json,
            project=config.project_id
        )
    
    return storage.Client(project=config.project_id)


def get_bucket(config: Optional[GCPStorageConfig] = None) -> storage.Bucket:
    """
    Return the configured bucket instance.

    Raises ValueError when the bucket name is missing because all storage
    operations require a target bucket.
    The bucket object is a lightweight handle; no network call is made here.
    """
    if config is None:
        config = GCPStorageConfig(
            bucket_name=DEFAULT_GCP_BUCKET,
            credentials_json=DEFAULT_GCP_CREDENTIALS_JSON,
            project_id=DEFAULT_GCP_PROJECT_ID,
        )

    if not config.bucket_name:
        raise ValueError("GCP bucket name is not configured.")

    client = get_storage_client(config)
    return client.bucket(config.bucket_name)


def upload_pdf(
    *,
    file_bytes: bytes,
    destination_path: str,
    content_type: str = "application/pdf",
    config: Optional[GCPStorageConfig] = None,
) -> str:
    """
    Upload raw PDF bytes to GCP and return the public URL.

    - file_bytes: raw PDF data (bytes)
    - destination_path: object path within the bucket
    - content_type: defaults to application/pdf
    - returns: public URL (requires bucket/object ACL or uniform access policy)
    """
    bucket = get_bucket(config)
    blob = bucket.blob(destination_path)
    blob.upload_from_string(file_bytes, content_type=content_type)
    return blob.public_url


def upload_pdf_fileobj(
    *,
    file_obj: BytesIO,
    destination_path: str,
    content_type: str = "application/pdf",
    config: Optional[GCPStorageConfig] = None,
) -> str:
    """
    Upload a PDF from a file-like object and return the public URL.

    Use this for streaming uploads (e.g., from Django file uploads).
    The file object must be opened in binary mode.
    """
    bucket = get_bucket(config)
    blob = bucket.blob(destination_path)
    blob.upload_from_file(file_obj, content_type=content_type)
    return blob.public_url


def download_pdf(
    *,
    source_path: str,
    config: Optional[GCPStorageConfig] = None,
) -> bytes:
    """
    Download a PDF from GCP and return it as raw bytes.

    - source_path: object path within the bucket
    - returns: bytes suitable for direct file writes or HTTP responses
    """
    bucket = get_bucket(config)
    blob = bucket.blob(source_path)
    return blob.download_as_bytes()


def download_pdf_to_fileobj(
    *,
    source_path: str,
    file_obj: BytesIO,
    config: Optional[GCPStorageConfig] = None,
) -> BytesIO:
    """
    Download a PDF into a file-like object.

    Returns the same file object (rewound to the start) for convenience.
    The file object must be writable and opened in binary mode.
    """
    bucket = get_bucket(config)
    blob = bucket.blob(source_path)
    blob.download_to_file(file_obj)
    file_obj.seek(0)
    return file_obj
