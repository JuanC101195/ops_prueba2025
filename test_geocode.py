import os
import pytest
from app.geocoding import geocode_one

pytestmark = pytest.mark.skipif(
    not (os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_MAPS_API_KEY")),
    reason="No Google API key configured"
)

def test_geocode_one():
    r = geocode_one('Carrera 70 # 26A - 33')
    print({k: r[k] for k in ['formatted_address', 'lat', 'lng', 'place_id', 'error']})
    # opcionalmente podrías validar algo, por ejemplo:
    assert r["error"] in ("", None)
    assert r["lat"] and r["lng"]
