from typing import List, Dict
import os
import time
import requests
from dotenv import load_dotenv, find_dotenv

# Cargar variables del .env (busca desde el cwd hacia arriba) y sobreescribe si ya existían
load_dotenv(find_dotenv(usecwd=True), override=True)

def _get_api_key() -> str:
    # Acepta ambos nombres por compatibilidad y también maneja BOM accidental
    candidates = [
        "GOOGLE_API_KEY",
        "GOOGLE_MAPS_API_KEY",
        "\ufeffGOOGLE_API_KEY",
        "\ufeffGOOGLE_MAPS_API_KEY",
    ]
    for c in candidates:
        v = os.getenv(c)
        if v:
            return v
    return ""

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

def geocode_one(address: str) -> Dict:
    api_key = _get_api_key()
    if not api_key:
        raise ValueError("Falta GOOGLE_API_KEY (o GOOGLE_MAPS_API_KEY) en .env o variables de entorno.")

    params = {"address": address, "key": api_key, "language": "es"}
    try:
        resp = requests.get(GEOCODE_URL, params=params, timeout=20)
        data = resp.json()
    except Exception as e:
        return {
            "address_input": address,
            "formatted_address": "",
            "lat": "",
            "lng": "",
            "place_id": "",
            "error": f"REQUEST_ERROR: {e}",
        }

    status = data.get("status", "NO_STATUS")
    if status == "OK" and data.get("results"):
        res = data["results"][0]
        loc = res["geometry"]["location"]
        return {
            "address_input": address,
            "formatted_address": res.get("formatted_address", ""),
            "lat": loc.get("lat", ""),
            "lng": loc.get("lng", ""),
            "place_id": res.get("place_id", ""),
            "error": "",
        }
    else:
        return {
            "address_input": address,
            "formatted_address": "",
            "lat": "",
            "lng": "",
            "place_id": "",
            "error": status,  # ZERO_RESULTS, REQUEST_DENIED, etc.
        }

def geocode_addresses(addresses: List[str]) -> List[Dict]:
    out: List[Dict] = []
    for a in addresses:
        out.append(geocode_one(a))
        time.sleep(0.1)
    return out
