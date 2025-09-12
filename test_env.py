from dotenv import load_dotenv, find_dotenv
import os
from app.geocoding import _get_api_key

def mask(x):
    return (x[:6] + '...' + x[-4:]) if x and len(x) > 10 else x

path = find_dotenv(usecwd=True)
ok = load_dotenv(path, override=True)
env_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GOOGLE_MAPS_API_KEY') or os.getenv('\ufeffGOOGLE_API_KEY') or os.getenv('\ufeffGOOGLE_MAPS_API_KEY')
print('find_dotenv ->', path)
print('load_dotenv ->', ok)
print('env key ->', mask(env_key))
print('_get_api_key() ->', mask(_get_api_key()))
