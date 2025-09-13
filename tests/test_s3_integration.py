import os
import pytest
from app.uploader import upload_files_to_s3

bucket = os.getenv("S3_BUCKET", "") or ""
prefix = (os.getenv("S3_PREFIX") or "").strip()
access = os.getenv("AWS_ACCESS_KEY_ID", "") or ""
secret = os.getenv("AWS_SECRET_ACCESS_KEY", "") or ""
region = os.getenv("AWS_DEFAULT_REGION", "") or ""

def _configured() -> bool:
    vals = [bucket, access, secret, region]
    if any(v in ("", "REMOVED") for v in vals):
        return False
    # Evita placeholders tipo "REMOVED"
    if "REMOVED" in (bucket.upper(), prefix.upper(), access.upper(), secret.upper(), region.upper()):
        return False
    return True

@pytest.mark.skipif(not _configured(), reason="S3 no configurado: test de integración saltado")
def test_s3_upload_sample():
    paths = ["sample_data/ejemplo.txt"]
    # No afirma nada: si no lanza excepción, consideramos OK.
    upload_files_to_s3(paths, bucket=bucket, prefix=prefix)
