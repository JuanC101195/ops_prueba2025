import argparse
import os

from . import config
from .uploader import upload_files_to_s3
from .extractor import extract_address
from .homonyms import generate_homonyms
from .similarity import score
from .geocoding import geocode_addresses
from .visualizer import save_map
from .storage import (
    save_list_to_txt, save_homonyms, save_similarity,
    unique_by_key, save_to_sqlite
)


def run_pipeline(inputs, workdir, use_s3, threshold: float = 90.0):
    os.makedirs(workdir, exist_ok=True)

    # 1) Subir a S3 si se pide
    if use_s3:
        upload_files_to_s3(inputs, bucket=config.S3_BUCKET, prefix=config.S3_PREFIX)

    # 2) Extraer dirección
    address = None
    extracted_text = None
    for p in inputs:
        addr, text = extract_address(p)
        extracted_text = text or extracted_text
        if addr:
            address = addr
            break

    if extracted_text:
        # Guarda el texto extraído del primer archivo procesado (útil para depurar)
        save_list_to_txt([extracted_text], os.path.join(workdir, "extracted.txt"))

    if not address:
        raise ValueError("No se encontró dirección en los documentos.")

    # 3) Generar homónimos
    homs = generate_homonyms(address)
    homs_base = os.path.join(workdir, "homonimos")
    save_homonyms(homs, homs_base)

    # 4) Filtrar por similitud
    filtered = []
    for h in homs:
        sc = score(address, h)
        if sc >= threshold:
            filtered.append({"original": address, "homonimo": h, "score": sc})
    filtered_base = os.path.join(workdir, "homonimos_filtrados")
    save_similarity(filtered, filtered_base)

    # Guardar en SQLite (nueva fuente de datos)
    sqlite_db = os.path.join(workdir, "resultados.db")
    save_to_sqlite(filtered, sqlite_db, "homonimos_filtrados")

    # 5) Geocoding
    addrs = [r["homonimo"] for r in filtered]
    geos = geocode_addresses(addrs)

    # ← Añadir score a cada fila geocodificada para que llegue al mapa
    score_by_addr = {r["homonimo"]: r["score"] for r in filtered}
    for g in geos:
        g["score"] = score_by_addr.get(g.get("address_input"))

    res_base = os.path.join(workdir, "resultados")
    save_similarity(geos, res_base)
    save_to_sqlite(geos, sqlite_db, "geocoding")

    # 6) Únicos
    uniques = unique_by_key(geos, "formatted_address")
    uni_base = os.path.join(workdir, "resultados_unicos")
    save_similarity(uniques, uni_base)
    save_to_sqlite(uniques, sqlite_db, "geocoding_unicos")

    # 7) Mapas
    save_map(geos, os.path.join(workdir, "mapa.html"))
    save_map(uniques, os.path.join(workdir, "mapa_unicos.html"))

    print("✅ Pipeline finalizado")
    print(f"Dirección base: {address}")
    print(f"Archivos en: {workdir}")


def main():
    parser = argparse.ArgumentParser(description="Prueba Técnica Operaciones - Pipeline")
    sub = parser.add_subparsers(dest="cmd")

    r = sub.add_parser("run", help="Ejecuta el pipeline completo")
    r.add_argument("--inputs", nargs="+", required=True, help="Archivos a procesar (PDF o TXT)")
    r.add_argument("--workdir", required=True, help="Directorio de salida")
    r.add_argument("--s3", action="store_true", help="Subir a S3 los archivos antes de procesar")
    r.add_argument("--threshold", type=float, default=90.0, help="Umbral de similitud (0-100)")

    args = parser.parse_args()
    if args.cmd == "run":
        run_pipeline(args.inputs, args.workdir, args.s3, args.threshold)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

