"""
S3/MinIO utility functions for object storage operations.
"""

import json
import logging
import os
from datetime import datetime
from typing import Any

import boto3
from botocore.exceptions import ClientError


def create_s3_client():
    """
    Create and return an S3 client.
    Uses AWS credentials from environment variables.
    """
    try:
        # Get S3 configuration from environment variables
        access_key = os.getenv("S3_ACCESS_KEY_ID")
        secret_key = os.getenv("S3_SECRET_ACCESS_KEY")
        endpoint_url = os.getenv("S3_ENDPOINT_URL")
        region = os.getenv("S3_REGION", "us-east-1")
        
        if not access_key or not secret_key:
            raise ValueError("S3_ACCESS_KEY_ID and S3_SECRET_ACCESS_KEY must be set in environment variables")
        
        # Create S3 client with environment variables
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url,
            region_name=region
        )
        
        logging.info(f"S3 client created successfully with endpoint: {endpoint_url}")
        return s3_client
    except Exception as e:
        logging.error(f"Error creating S3 client: {str(e)}")
        raise


def upload_json_to_s3(data: dict[str, Any], bucket_name: str, object_key: str) -> str:
    """
    Upload JSON data to S3.

    Args:
        data: Dictionary to upload as JSON
        bucket_name: S3 bucket name
        object_key: S3 object key (file path)

    Returns:
        S3 URI of the uploaded object
    """
    try:
        s3_client = create_s3_client()

        # Convert data to JSON string
        json_data = json.dumps(data, indent=2, ensure_ascii=False)

        # Upload to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=json_data,
            ContentType="application/json",
        )

        s3_uri = f"s3://{bucket_name}/{object_key}"
        logging.info(f"Successfully uploaded data to {s3_uri}")
        return s3_uri

    except ClientError as e:
        logging.error(f"AWS S3 error uploading to {bucket_name}/{object_key}: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error uploading to S3: {str(e)}")
        raise


def generate_s3_key(timestamp: str, data_type: str = "pokemon") -> str:
    """
    Generate an S3 object key with timestamp partitioning.

    Args:
        timestamp: ISO timestamp string
        data_type: Type of data for the key prefix

    Returns:
        S3 object key with date partitioning
    """
    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

    # Create partitioned key: data_type/year=YYYY/month=MM/day=DD/filename
    key = (
        f"{data_type}/"
        f"year={dt.year}/"
        f"month={dt.month:02d}/"
        f"day={dt.day:02d}/"
        f"{data_type}_{dt.strftime('%Y%m%d_%H%M%S')}.json"
    )

    return key
