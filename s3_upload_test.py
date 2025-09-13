from app.uploader import upload_files_to_s3
import os

bucket = os.getenv("S3_BUCKET")
prefix = os.getenv("S3_PREFIX") or ""
prefix = prefix.strip()  # si era " " lo dejamos vacío

print("Bucket:", bucket)
print("Prefix:", repr(prefix))

# Archivo de prueba
paths = ["sample_data/ejemplo.txt"]
upload_files_to_s3(paths, bucket=bucket, prefix=prefix)

print("✅ Archivo subido correctamente a S3")
