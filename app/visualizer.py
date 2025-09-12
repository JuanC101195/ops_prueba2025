# app/visualizer.py
from typing import Iterable
import folium

def save_map(points: Iterable[dict], out_html: str = "mapa.html") -> None:
    pts = [p for p in points if p.get("lat") is not None and p.get("lng") is not None]
    if not pts:
        raise ValueError("No hay puntos con coordenadas para el mapa.")

    # Centro del mapa en el promedio de los puntos
    avg_lat = sum(p["lat"] for p in pts) / len(pts)
    avg_lng = sum(p["lng"] for p in pts) / len(pts)
    m = folium.Map(location=[avg_lat, avg_lng], zoom_start=12)

    for p in pts:
        s = p.get("score")
        score_txt_html = f"<br/>Score: {s:.1f}" if isinstance(s, (int, float)) else ""
        score_txt_tip = f" | score {s:.1f}" if isinstance(s, (int, float)) else ""

        addr = p.get("formatted_address") or p.get("address_input") or "Sin dirección"
        lat = float(p["lat"])
        lng = float(p["lng"])

        popup_text = (
            f"{addr}<br/>(Lat: {lat:.6f}, Lng: {lng:.6f})"
            f"{score_txt_html}"
        )
        tooltip_text = f'{p.get("address_input") or addr} ({lat:.4f}, {lng:.4f}){score_txt_tip}'

        folium.Marker(
            [lat, lng],
            popup=popup_text,
            tooltip=tooltip_text
        ).add_to(m)

    m.save(out_html)

