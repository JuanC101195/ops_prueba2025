import os
import requests
from typing import List, Dict

def geocode_addresses(addresses: List[str]) -> List[Dict]:
    """
    Recibe una lista de direcciones en texto plano y devuelve
    una lista de diccionarios con lat, lng, place_id y la dirección formateada.
    """

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Falta GOOGLE_API_KEY en el .env")

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    results = []

    for addr in addresses:
        params = {"address": addr, "key": api_key}
        resp = requests.get(url, params=params)

        if resp.status_code != 200:
            results.append({
                "address_input": addr,
                "formatted_address": None,
                "lat": None,
                "lng": None,
                "place_id": None,
                "error": f"HTTP {resp.status_code}"
            })
            continue

        data = resp.json()
        if data.get("status") != "OK":
            results.append({
                "address_input": addr,
                "formatted_address": None,
                "lat": None,
                "lng": None,
                "place_id": None,
                "error": data.get("status")
            })
            continue

        info = data["results"][0]
        loc = info["geometry"]["location"]
        results.append({
            "address_input": addr,
            "formatted_address": info.get("formatted_address"),
            "lat": loc.get("lat"),
            "lng": loc.get("lng"),
            "place_id": info.get("place_id"),
            "error": None
        })

    return results
