import pandas as pd
from pathlib import Path

WD = Path(r'.\workdir\from_s3')

paths = {
    "homonimos": WD/'homonimos.csv',
    "filtrados": WD/'homonimos_filtrados.csv',
    "resultados": WD/'resultados.csv',
    "unicos": WD/'resultados_unicos.csv',
    "mapa": WD/'mapa.html',
    "mapa_unicos": WD/'mapa_unicos.html',
    "sqlite": WD/'resultados.db',
}

def exists_report(label, p: Path):
    return f"[{'OK' if p.exists() else 'NO'}] {label}: {p}"

# 1) Existencia de archivos clave
print("=== Existencia de artefactos ===")
for k,p in paths.items():
    print(exists_report(k, p))

# 2) Cargas principales
df_h = pd.read_csv(paths["homonimos"]) if paths["homonimos"].exists() else pd.DataFrame()
df_f = pd.read_csv(paths["filtrados"]) if paths["filtrados"].exists() else pd.DataFrame()
df_r = pd.read_csv(paths["resultados"]) if paths["resultados"].exists() else pd.DataFrame()
df_u = pd.read_csv(paths["unicos"]) if paths["unicos"].exists() else pd.DataFrame()

print("\n=== Conteos ===")
print("Homónimos generados:", len(df_h))
print("Homónimos filtrados (>=90):", len(df_f))
print("Filas geocodificadas:", len(df_r))
print("Filas únicas por formatted_address:", len(df_u))

# 3) Validaciones de calidad en resultados.csv
ok_geocoding = False
if not df_r.empty:
    # Columnas esperadas
    cols = {"address_input","formatted_address","lat","lng","place_id","error","score"}
    missing = cols - set(df_r.columns)
    if missing:
        print("\n[WARN] Faltan columnas en resultados.csv:", missing)

    # a) scores = 100
    all_100 = False
    if "score" in df_r.columns:
        try:
            scores = pd.to_numeric(df_r["score"], errors="coerce")
            all_100 = scores.fillna(0).eq(100).all()
        except Exception as e:
            print("[WARN] No se pudo procesar score:", e)
    print("Todos los score = 100:", all_100)

    # b) sin errores
    err_count = 0
    if "error" in df_r.columns:
        err_count = df_r["error"].fillna("").astype(str).str.strip().ne("").sum()
    print("Filas con error != '' :", err_count)

    # c) lat/lng presentes
    coords_ok = False
    try:
        lat_ok = pd.to_numeric(df_r["lat"], errors="coerce").notna()
        lng_ok = pd.to_numeric(df_r["lng"], errors="coerce").notna()
        coords_ok = (lat_ok & lng_ok).all()
    except Exception as e:
        print("[WARN] No se pudo validar lat/lng:", e)
    print("Todas las filas tienen lat/lng:", coords_ok)

    # d) únicos por address y place_id
    unique_addr = df_r["formatted_address"].nunique(dropna=True) if "formatted_address" in df_r.columns else 0
    unique_pid  = df_r["place_id"].nunique(dropna=True) if "place_id" in df_r.columns else 0
    print("Unique formatted_address:", unique_addr)
    print("Unique place_id:", unique_pid)

    ok_geocoding = all_100 and err_count == 0 and coords_ok

# 4) Previews
def preview(df, title, n=5):
    print(f"\n--- {title} (primeras {n}) ---")
    if df.empty:
        print("(vacío)")
    else:
        print(df.head(n).to_string(index=False))

preview(df_f, "homonimos_filtrados.csv", 10)
preview(df_r[["address_input","formatted_address","lat","lng","score"]] if not df_r.empty else df_r, "resultados.csv", 10)
preview(df_u[["address_input","formatted_address","lat","lng","score"]] if not df_u.empty else df_u, "resultados_unicos.csv", 10)

# 5) Resumen final
print("\n=== RESUMEN ===")
print("Archivos OK:", all(p.exists() for k,p in paths.items() if k in ["homonimos","filtrados","resultados","unicos","mapa","mapa_unicos"]))
print("Validación geocoding OK (score=100, sin errores, lat/lng presentes):", ok_geocoding)
