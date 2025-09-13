# regeocode_failed.py
import os, time
import pandas as pd
from dotenv import load_dotenv
from app.geocoding import geocode_one
from app.visualizer import save_map
from pathlib import Path

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
        return (x is None) or (str(x).strip() == "")
    return (err != "") or empty(lat) or empty(lng)

mask = df.apply(needs_fix, axis=1)
todo = df[mask].copy()

print(f"Filas totales: {len(df)}  |  A reintentar: {len(todo)}")
if not len(todo):
    print("Nada por reintentar. Saliendo.")
else:
    fixed = 0
    for i, row in todo.iterrows():
        addr = row["address_input"]
        try:
            r = geocode_one(addr)
            # actualiza columnas
            for k in ["formatted_address","lat","lng","place_id","error"]:
                df.at[i, k] = r.get(k, df.at[i,k])
            fixed += 1
            time.sleep(0.2)  # pequeña pausa
        except Exception as e:
            df.at[i,"error"] = f"RETRY_ERROR: {e}"

    df.to_csv(csv_result, index=False)
    print(f"✅ Reintentos aplicados y guardados: {fixed}")

# Recalcular únicos por formatted_address
if "formatted_address" in df.columns:
    dfu = df.sort_values("formatted_address").drop_duplicates("formatted_address")
else:
    dfu = df.copy()

dfu.to_csv(csv_unicos, index=False)

# Regenerar mapas
save_map(df.to_dict("records"), str(html_mapa))
save_map(dfu.to_dict("records"), str(html_mapa_u))

print("✅ Mapas regenerados.")
