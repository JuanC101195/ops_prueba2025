# verify_s3_source.py
# Valida que el archivo procesado proviene del S3 object (comparando hashes),
# muestra la dirección extraída desde ese archivo y evidencia de pipeline.

import os, hashlib, boto3, pandas as pd
from pathlib import Path
from app.extractor import extract_address

BUCKET = os.getenv("S3_BUCKET") or "ops-prueba-juan-20250912"
REGION = os.getenv("AWS_DEFAULT_REGION") or "us-east-2"
KEY    = "uploads/ejemplo_s3.txt"  # donde lo subimos en s3_flow
LOCAL_SRC  = Path(r"sample_data/ejemplo.txt")                    # fuente original local (antes de subir)
LOCAL_S3DL = Path(r".\workdir\from_s3\s3_inputs\ejemplo_s3.txt") # descargado de S3 y usado por pipeline

def md5sum(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

print("== Verificación de origen S3 ==")
print("Bucket:", BUCKET)
print("Key   :", KEY)
print("Local original       :", LOCAL_SRC, "existe:", LOCAL_SRC.exists())
print("Local descargado S3  :", LOCAL_S3DL, "existe:", LOCAL_S3DL.exists())

if not LOCAL_S3DL.exists():
    raise SystemExit("❌ No existe el archivo descargado desde S3.")

# 1) MD5 local vs ETag y MD5 vs MD5 (para archivos pequeños ETag = MD5)
s3 = boto3.client("s3", region_name=REGION)
head = s3.head_object(Bucket=BUCKET, Key=KEY)
etag = head["ETag"].strip('"')

md5_local_src  = md5sum(LOCAL_SRC)  if LOCAL_SRC.exists() else None
md5_local_s3dl = md5sum(LOCAL_S3DL)

print("\n— Checksums —")
print("ETag (S3)          :", etag)
print("MD5 local fuente   :", md5_local_src)
print("MD5 local descargado:", md5_local_s3dl)

etag_match = (etag == md5_local_s3dl)
src_match  = (md5_local_src == md5_local_s3dl) if md5_local_src else None
print("¿ETag S3 == MD5 descargado?      ", etag_match)
print("¿MD5 fuente == MD5 descargado?   ", src_match)

# 2) Dirección extraída desde el archivo descargado (la que usa el pipeline)
addr, raw_text = extract_address(str(LOCAL_S3DL))
print("\n— Dirección extraída del archivo S3 descargado —")
print("Dirección:", addr if addr else "(no detectada)")
print("Texto (primeros 120 chars):", (raw_text[:120] + "...") if raw_text else "(sin texto)")

# 3) Evidencia de pipeline: archivos y primeras filas
WD = Path(r".\workdir\from_s3")
csv_res = WD / "resultados.csv"
csv_fil = WD / "homonimos_filtrados.csv"
print("\n— Evidencia de pipeline —")
print("resultados.csv existe:", csv_res.exists())
print("homonimos_filtrados.csv existe:", csv_fil.exists())

if csv_fil.exists():
    dff = pd.read_csv(csv_fil)
    print("Filtrados (>=90):", len(dff))
    print(dff.head(3).to_string(index=False))

if csv_res.exists():
    dfr = pd.read_csv(csv_res)
    print("\nresultados.csv (head):")
    cols = [c for c in ["address_input","formatted_address","lat","lng","score","error"] if c in dfr.columns]
    print(dfr[cols].head(3).to_string(index=False))
