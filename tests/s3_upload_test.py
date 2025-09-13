import os
import pytest
from app.uploader import upload_files_to_s3

def _is_configured() -> bool:
    bucket = os.getenv("S3_BUCKET") or ""
    access = os.getenv("AWS_ACCESS_KEY_ID") or ""
    secret = os.getenv("AWS_SECRET_ACCESS_KEY") or ""
    region = os.getenv("AWS_DEFAULT_REGION") or ""

    def bad(v: str) -> bool:
        u = v.strip().upper()
        return (u == "" or u == "REMOVED" or "REMOVED" in u)

    # Requerimos bucket, access, secret y region reales
    return not any(bad(v) for v in (bucket, access, secret, region))

@pytest.mark.skipif(not _is_configured(), reason="S3 no configurado (sin credenciales reales) → test saltado")
def test_s3_upload_sample(tmp_path):
    # Crea archivo temporal y hace upload solo si hay credenciales reales
    f = tmp_path / "ejemplo.txt"
    f.write_text("Archivo de prueba para S3")
    bucket = os.getenv("S3_BUCKET") or ""
    prefix = (os.getenv("S3_PREFIX") or "").strip()
    upload_files_to_s3([str(f)], bucket=bucket, prefix=prefix)
