from app.visualizer import save_map
import pandas as pd

df = pd.read_excel('.\\workdir\\resultados.xlsx').to_dict('records')
save_map(df, '.\\workdir\\mapa.html')

dfu = pd.read_excel('.\\workdir\\resultados_unicos.xlsx').to_dict('records')
save_map(dfu, '.\\workdir\\mapa_unicos.html')

print("Mapas regenerados con coordenadas en popup.")
