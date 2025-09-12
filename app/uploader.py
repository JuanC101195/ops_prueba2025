from typing import Iterable, List, Optional
import os
import boto3
from . import config

def upload_files_to_s3(paths: Iterable[str], bucket: Optional[str] = None, prefix: Optional[str] = None) -> List[str]:
    bucket = bucket or config.S3_BUCKET
    prefix = prefix or config.S3_PREFIX
    if not bucket:
        raise ValueError("S3 bucket no definido. Configura S3_BUCKET en el .env o pasa bucket explícitamente.")
    s3 = boto3.client("s3", region_name=config.AWS_DEFAULT_REGION)
    keys = []
    for p in paths:
        key = f"{prefix.strip('/')}/{os.path.basename(p)}"
        s3.upload_file(p, bucket, key)
        keys.append(key)
    return keys
