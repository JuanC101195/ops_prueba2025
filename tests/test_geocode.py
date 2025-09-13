import os
import pytest
from dotenv import load_dotenv, find_dotenv
from app.geocoding import geocode_one

load_dotenv(find_dotenv(usecwd=True), override=True)
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_MAPS_API_KEY")

@pytest.mark.skipif(not api_key, reason="GOOGLE_API_KEY no configurada: se salta geocoding")
def test_geocode_smoke():
    r = geocode_one("Carrera 70 # 26A - 33")
    # Validaciones básicas
    assert r.get("error", "") == ""
    assert r.get("formatted_address", "")
    assert r.get("lat") not in (None, "")
    assert r.get("lng") not in (None, "")
