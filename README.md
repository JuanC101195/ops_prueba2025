# Prueba Técnica – Operaciones

Este proyecto implementa un **pipeline de procesamiento de direcciones** que:

1. Extrae una dirección desde un archivo de entrada (PDF o TXT).
2. Genera **homónimos** (variantes de la dirección).
3. Calcula **similitud** con la dirección original y filtra por umbral ≥90.
4. Geocodifica las direcciones filtradas con la API de Google Maps.
5. Guarda resultados en **CSV, XLSX y SQLite**.
6. Visualiza en mapas interactivos con **Folium** (HTML).

---

## 📦 Requisitos

- Python 3.10+
- Cuenta de Google Cloud con **API Key de Geocoding**
- (Opcional) AWS S3 configurado si se usa la subida de archivos

Instalar dependencias:

`ash
pip install -r requirements.txt

Configurar variables de entorno (.env):
GOOGLE_API_KEY=tu_api_key_aqui
S3_BUCKET=mi-bucket (opcional)
S3_PREFIX=ops (opcional)

▶️ Uso

Ejecutar el pipeline:
python -m app.main run 
  --inputs .\sample_data\ejemplo.txt 
  --workdir .\workdir 
  --threshold 90

--inputs: archivo(s) de entrada (PDF o TXT)

--workdir: directorio de salida

--threshold: umbral de similitud (default 90)

--s3: opcional, subir a S3 antes de procesar

📂 Archivos generados

En el directorio workdir/ encontrarás:

homonimos.csv / .xlsx: lista completa de homónimos

homonimos_filtrados.csv / .xlsx: homónimos con score ≥90

resultados.csv / .xlsx: direcciones geocodificadas

resultados_unicos.csv / .xlsx: resultados únicos por dirección formateada

resultados.db: base de datos SQLite con 3 tablas:

homonimos_filtrados

geocoding

geocoding_unicos

mapa.html y mapa_unicos.html: mapas interactivos con pines

✅ Validación del filtro

Script incluido: validate_filter.py

Ejecutar:
python .\validate_filter.py

Resultado esperado:

Los 60 homónimos buenos pasan (score=100).

Casos artificiales “malos” (Carrera 71…, Calle 70…, Bogotá…) no pasan (score <90).

📊 Ejemplo de salida
Umbral = 90
PASARON: 60 de 65
NO PASARON: 5

--- Ejemplos que PASAN ---
[GOOD] Carrera 70 # 26A - 33  -> score=100.0
[GOOD] Carrera 70 No 26A 33   -> score=100.0

--- Ejemplos que NO PASAN ---
[BAD] Av 70 # 26A - 33, Bogota  -> score=83.3

🌍 Mapas

Abrir los mapas generados en navegador:
Start-Process .\workdir\mapa.html
Start-Process .\workdir\mapa_unicos.html

Cada pin muestra:

Dirección formateada

Coordenadas (lat, lng)

Score de similitud

🧪 Tests

Ejecutar pruebas unitarias:
pytest -q
Incluye pruebas de similitud y validación del filtro.

👤 Autor Juan Esteban Cardozo Rivera
Proyecto desarrollado como parte de la Prueba Técnica de Operaciones 2025.
