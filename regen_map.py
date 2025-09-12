# regen_map.py — lee CSV o XLSX automáticamente y regenera los mapas
from pathlib import Path
import pandas as pd
from app.visualizer import save_map

WD = Path("workdir")

def read_table(base: str):
    csv  = WD / f"{base}.csv"
    xlsx = WD / f"{base}.xlsx"
    if csv.exists():
        return pd.read_csv(csv).to_dict("records")
    if xlsx.exists():
        return pd.read_excel(xlsx).to_dict("records")
    raise FileNotFoundError(f"No existe {csv} ni {xlsx}")

if __name__ == "__main__":
    res = read_table("resultados")
    save_map(res, str(WD / "mapa.html"))

    uni = read_table("resultados_unicos")
    save_map(uni, str(WD / "mapa_unicos.html"))

    print("✅ Mapas regenerados con coordenadas y score en popup.")
