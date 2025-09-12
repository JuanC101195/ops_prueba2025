# app/visualizer.py
from typing import Iterable, Any
import html
import folium
import math

def _to_float(v: Any):
    try:
        f = float(v)
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    except Exception:
        return None

def save_map(points: Iterable[dict], out_html: str = "mapa.html") -> None:
    # Normaliza/filtra coordenadas: no None, no NaN, no Inf
    pts = []
    for p in points:
        lat = _to_float(p.get("lat"))
        lng = _to_float(p.get("lng"))
        if lat is None or lng is None:
            continue
        q = dict(p)
        q["lat"], q["lng"] = lat, lng
        pts.append(q)

    if not pts:
        raise ValueError("No hay puntos con coordenadas para el mapa.")

    avg_lat = sum(p["lat"] for p in pts) / len(pts)
    avg_lng = sum(p["lng"] for p in pts) / len(pts)
    m = folium.Map(location=[avg_lat, avg_lng], zoom_start=12)

    for p in pts:
        s = _to_float(p.get("score"))
        score_html = f"<br/>Score: {s:.1f}" if s is not None else ""
        score_tip  = f" | score {s:.1f}"   if s is not None else ""

        addr = p.get("formatted_address") or p.get("address_input") or "Sin dirección"
        addr = html.escape(str(addr))
        lat, lng = p["lat"], p["lng"]

        popup_text = f"{addr}<br/>(Lat: {lat:.6f}, Lng: {lng:.6f}){score_html}"
        tooltip_text = f'{p.get("address_input") or addr} ({lat:.4f}, {lng:.4f}){score_tip}'

        folium.Marker([lat, lng], popup=popup_text, tooltip=tooltip_text).add_to(m)

    m.save(out_html)
