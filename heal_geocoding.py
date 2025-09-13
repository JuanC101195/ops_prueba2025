# heal_geocoding.py
import os, time, re
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from app.geocoding import geocode_one
from app.visualizer import save_map

load_dotenv()
WD = Path(r'.\workdir\from_s3')
csv_result = WD/'resultados.csv'
csv_unicos = WD/'resultados_unicos.csv'
html_mapa  = WD/'mapa.html'
html_mapa_u= WD/'mapa_unicos.html'

if not csv_result.exists():
    raise SystemExit(f"No existe {csv_result}")

df = pd.read_csv(csv_result)

def needs_fix(row):
    err = str(row.get("error", "")).strip()
    lat = row.get("lat", "")
    lng = row.get("lng", "")
    def empty(x): 
        return (x is None) or (str(x).strip() == "") or (str(x).lower() == "nan")
    return (err != "") or empty(lat) or empty(lng)

def normalize_addr(s: str) -> str:
    if not s: 
        return s
    t = s.strip()
    # normalizaciones comunes Colombia
    # Kra/Kr -> Cra
    t = re.sub(r'\b(Kra?|KRA?)\b', 'Cra', t, flags=re.IGNORECASE)
    # Numero variantes -> '#'
    t = re.sub(r'\b(N[úu]m(?:ero)?|Nro|No\.?|Num)\b', '#', t, flags=re.IGNORECASE)
    # limpiar dobles espacios
    t = re.sub(r'\s+', ' ', t).strip()
    # si falta ciudad/país, agrega contexto para ayudar al geocoder
    if 'Medell' not in t and 'Bogot' not in t and 'Colombia' not in t:
        t = f"{t}, Medellín, Antioquia, Colombia"
    return t

mask = df.apply(needs_fix, axis=1)
todo = df[mask].copy()

print(f"Filas totales: {len(df)}  |  A reparar: {len(todo)}")
if not len(todo):
    print("Nada por reparar. Saliendo.")
else:
    fixed, still_bad = 0, 0
    for i, row in todo.iterrows():
        raw = str(row["address_input"])
        cand = normalize_addr(raw)
        ok = False
        for attempt in range(1, 4):  # hasta 3 intentos con backoff
            r = geocode_one(cand)
            err = str(r.get("error","")).strip()
            lat = r.get("lat", "")
            lng = r.get("lng", "")
            # éxito si hay lat/lng y sin error
            if err == "" and str(lat).strip() not in ("","nan") and str(lng).strip() not in ("","nan"):
                # actualizar fila
                for k in ["address_input","formatted_address","lat","lng","place_id","error"]:
                    # mantenemos address_input original, actualizamos lo demás
                    if k == "address_input":
                        continue
                    df.at[i, k] = r.get(k, df.at[i,k])
                fixed += 1
                ok = True
                break
            time.sleep(0.4 * attempt)  # backoff ligero

        if not ok:
            # último intento: agregar explícitamente ", Colombia" si no está
            if "Colombia" not in cand:
                r = geocode_one(cand + ", Colombia")
                err = str(r.get("error","")).strip()
                lat = r.get("lat", "")
                lng = r.get("lng", "")
                if err == "" and str(lat).strip() not in ("","nan") and str(lng).strip() not in ("","nan"):
                    for k in ["formatted_address","lat","lng","place_id","error"]:
                        df.at[i, k] = r.get(k, df.at[i,k])
                    fixed += 1
                    ok = True

        if not ok:
            still_bad += 1
            df.at[i,"error"] = err or "ZERO_RESULTS"

    df.to_csv(csv_result, index=False)
    print(f"✅ Reparadas: {fixed}  |  Pendientes: {still_bad}")

# recomputar únicos por formatted_address (descartando NaN)
if "formatted_address" in df.columns:
    dfu = df.dropna(subset=["formatted_address"]).sort_values("formatted_address").drop_duplicates("formatted_address")
else:
    dfu = df.copy()

dfu.to_csv(csv_unicos, index=False)

# Re-generar mapas solo con filas válidas (lat/lng numéricos)
def to_valid_records(df):
    try:
        d = df.copy()
        d["lat"] = pd.to_numeric(d["lat"], errors="coerce")
        d["lng"] = pd.to_numeric(d["lng"], errors="coerce")
        d = d.dropna(subset=["lat","lng"])
        return d.to_dict("records")
    except Exception:
        return []

valid_all   = to_valid_records(df)
valid_unico = to_valid_records(dfu)

if valid_all:
    save_map(valid_all, str(html_mapa))
if valid_unico:
    save_map(valid_unico, str(html_mapa_u))

print("✅ Mapas regenerados (solo con filas válidas).")
