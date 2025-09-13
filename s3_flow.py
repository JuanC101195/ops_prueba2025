import os, boto3, pathlib

bucket = os.getenv("S3_BUCKET") or "ops-prueba-juan-20250912"
region = os.getenv("AWS_DEFAULT_REGION") or "us-east-2"
key    = "uploads/ejemplo_s3.txt"   # ruta destino en S3

s3 = boto3.client("s3", region_name=region)

# 1) Subir archivo local a S3
src = r"sample_data/ejemplo.txt"
s3.upload_file(src, bucket, key)
print(f"✅ Subida OK: s3://{bucket}/{key}")

# 2) Listar objetos (evidencia)
resp = s3.list_objects_v2(Bucket=bucket, Prefix="uploads/")
print("📄 Objetos en s3://%s/uploads/:" % bucket)
for obj in resp.get("Contents", [])[:10]:
    print(" -", obj["Key"], obj["Size"], "bytes")

# 3) Descargar a carpeta local para procesar
out = pathlib.Path("workdir") / "s3_inputs" / "ejemplo_s3.txt"
out.parent.mkdir(parents=True, exist_ok=True)
s3.download_file(bucket, key, str(out))
print("⬇️  Descargado a:", out)
