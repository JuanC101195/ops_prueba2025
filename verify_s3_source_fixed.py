# verify_s3_source_fixed.py
import os, hashlib, boto3, pandas as pd
from pathlib import Path
from app.extractor import extract_address

BUCKET = os.getenv("S3_BUCKET") or "ops-prueba-juan-20250912"
REGION = os.getenv("AWS_DEFAULT_REGION") or "us-east-2"
KEY    = "uploads/ejemplo_s3.txt"

LOCAL_SRC   = Path(r"sample_data/ejemplo.txt")  # fuente original local
CANDIDATES  = [
    Path(r".\workdir\s3_inputs\ejemplo_s3.txt"),        # ruta correcta (donde s3_flow lo guardó)
    Path(r".\workdir\from_s3\s3_inputs\ejemplo_s3.txt") # ruta que intentamos antes
]

def md5sum(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

print("== Verificación de origen S3 ==")
print("Bucket:", BUCKET)
print("Key   :", KEY)

local_s3dl = None
for p in CANDIDATES:
    if p.exists():
        local_s3dl = p
        break

# Si no existe en ninguna de las rutas, re-descargarlo a la ruta correcta
if local_s3dl is None:
    local_s3dl = CANDIDATES[0]  # .\workdir\s3_inputs\ejemplo_s3.txt
    local_s3dl.parent.mkdir(parents=True, exist_ok=True)
    s3 = boto3.client("s3", region_name=REGION)
    s3.download_file(BUCKET, KEY, str(local_s3dl))
    print("⬇️  Re-descargado desde S3 a:", local_s3dl)

print("Local original        :", LOCAL_SRC, "existe:", LOCAL_SRC.exists())
print("Local descargado S3   :", local_s3dl, "existe:", local_s3dl.exists())

if not local_s3dl.exists():
    raise SystemExit("❌ No existe el archivo descargado desde S3.")

# 1) MD5 vs ETag (para archivos pequeños ETag = MD5)
s3 = boto3.client("s3", region_name=REGION)
head = s3.head_object(Bucket=BUCKET, Key=KEY)
etag = head["ETag"].strip('"')

md5_local_src  = md5sum(LOCAL_SRC)  if LOCAL_SRC.exists() else None
md5_local_s3dl = md5sum(local_s3dl)

print("\n— Checksums —")
print("ETag (S3)             :", etag)
print("MD5 local fuente      :", md5_local_src)
print("MD5 local descargado  :", md5_local_s3dl)
print("¿ETag S3 == MD5 descargado?     ", etag == md5_local_s3dl)
print("¿MD5 fuente == MD5 descargado?  ", (md5_local_src == md5_local_s3dl) if md5_local_src else None)

# 2) Dirección extraída del archivo S3 descargado
addr, raw_text = extract_address(str(local_s3dl))
print("\n— Dirección extraída del archivo S3 descargado —")
print("Dirección:", addr if addr else "(no detectada)")
print("Texto (primeros 120 chars):", (raw_text[:120] + "...") if raw_text else "(sin texto)")

# 3) Evidencia de pipeline
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
    cols = [c for c in ["address_input","formatted_address","lat","lng","score","error"] if c in dfr.columns]
    print("\nresultados.csv (head):")
    print(dfr[cols].head(3).to_string(index=False))
