from app.geocoding import geocode_one
r = geocode_one('Carrera 70 # 26A - 33')
print({k:r[k] for k in ['formatted_address','lat','lng','place_id','error']})
