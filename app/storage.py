from typing import List, Dict
import pandas as pd
import sqlite3
import os


def _ensure_parent_dir(path: str) -> None:
    """Crea el directorio padre si aplica (ignora si no hay)."""
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)


def save_list_to_txt(lines: List[str], path: str) -> None:
    """Guarda una lista de strings a TXT (una línea por elemento)."""
    _ensure_parent_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(f"{line}\n")


def _save_df_multi(df: pd.DataFrame, basepath_no_ext: str) -> None:
    """
    Guarda el DataFrame en CSV y XLSX usando el mismo 'basepath' sin extensión.
    Ej.: basepath_no_ext='workdir/homonimos' -> crea homonimos.csv y homonimos.xlsx
    """
    _ensure_parent_dir(basepath_no_ext)
    df.to_csv(basepath_no_ext + ".csv", index=False, encoding="utf-8")
    df.to_excel(basepath_no_ext + ".xlsx", index=False)


def save_homonyms(homonyms: List[str], basepath_no_ext: str) -> None:
    """Guarda la lista de homónimos en CSV y XLSX."""
    df = pd.DataFrame({"homonimos": homonyms})
    _save_df_multi(df, basepath_no_ext)


def save_similarity(rows: List[Dict], basepath_no_ext: str) -> None:
    """Guarda filas (diccionarios) de resultados/similitud/geocoding en CSV y XLSX."""
    df = pd.DataFrame(rows)
    _save_df_multi(df, basepath_no_ext)


def unique_by_key(rows: List[Dict], key: str) -> List[Dict]:
    """Devuelve filas únicas según la clave dada (primera ocurrencia gana)."""
    seen = set()
    out: List[Dict] = []
    for r in rows:
        v = r.get(key)
        if v and v not in seen:
            seen.add(v)
            out.append(r)
    return out


def save_to_sqlite(rows: List[Dict], db_path: str, table: str) -> None:
    """
    Guarda filas (diccionarios) en una tabla SQLite.
    - Crea la BD si no existe.
    - Reemplaza la tabla si ya existe.
    """
    _ensure_parent_dir(db_path)
    df = pd.DataFrame(rows)
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table, conn, if_exists="replace", index=False)

