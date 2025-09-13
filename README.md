# 🚀 Prueba Técnica – Operaciones 2025  

[![Tests](https://github.com/JuanC101195/ops_prueba2025/actions/workflows/tests.yml/badge.svg)](https://github.com/JuanC101195/ops_prueba2025/actions/workflows/tests.yml)  
![Version](https://img.shields.io/badge/version-v1.0.0-blue)  
![License](https://img.shields.io/badge/license-MIT-lightgrey)  

📌 Pipeline para procesamiento, normalización y geocodificación de direcciones.  

---

## 📑 Contenido
- Requisitos  
- Uso  
- Archivos generados  
- Validación del filtro  
- Ejemplo de salida  
- Mapas  
- Tests  
- Uso con AWS S3  
- Autor  

---

## 📦 Requisitos
- Python 3.10+  
- Cuenta de Google Cloud con **API Key de Geocoding**  
- (Opcional) AWS S3 configurado si se usa la subida de archivos  

Instalar dependencias:  

```bash
pip install -r requirements.txt
```

Configurar variables de entorno (`.env`):  

```bash
GOOGLE_API_KEY=your_api_key_here
S3_BUCKET=
S3_PREFIX=
```

**Importante:**  
- Las credenciales no se incluyen en este repo (por seguridad).  
- Si desea ejecutar con S3, debe configurar sus propias credenciales.  

Ejecutar el pipeline:  

```bash
python -m app.main run   --inputs ./sample_data/ejemplo.txt   --workdir ./workdir   --threshold 90
```

Parámetros:  
- `--inputs`: archivo(s) de entrada (PDF o TXT)  
- `--workdir`: directorio de salida  
- `--threshold`: umbral de similitud (default 90)  
- `--s3`: opcional, subir a S3 antes de procesar  

---

## 📂 Archivos generados
En el directorio `workdir/` encontrarás:  

- `homonimos.csv` / `.xlsx`: lista completa de homónimos  
- `homonimos_filtrados.csv` / `.xlsx`: homónimos con score ≥90  
- `resultados.csv` / `.xlsx`: direcciones geocodificadas  
- `resultados_unicos.csv` / `.xlsx`: resultados únicos por dirección formateada  
- `resultados.db`: base de datos SQLite con 3 tablas (`homonimos_filtrados`, `geocoding`, `geocoding_unicos`)  
- `mapa.html` y `mapa_unicos.html`: mapas interactivos con pines  

---

## 🧪 Validación del filtro
Script incluido: `validate_filter.py`  

Ejecutar:  

```bash
python ./validate_filter.py
```

Resultado esperado:  
- Los 60 homónimos buenos pasan (score=100).  
- Casos artificiales “malos” no pasan (score <90).  

---

## 📊 Ejemplo de salida
```text
Umbral = 90
PASARON: 60 de 65
NO PASARON: 5

--- Ejemplos que PASAN ---
[GOOD] Carrera 70 # 26A - 33  -> score=100.0
[GOOD] Carrera 70 No 26A 33   -> score=100.0

--- Ejemplos que NO PASAN ---
[BAD] Av 70 # 26A - 33, Bogota  -> score=83.3
```

---

## 🗺️ Mapas
Abrir los mapas generados en navegador:  

```bash
Start-Process ./workdir/mapa.html
Start-Process ./workdir/mapa_unicos.html
```

Cada pin muestra:  
- Dirección formateada  
- Coordenadas (lat, lng)  
- Score de similitud  

---

## 🧪 Tests
Ejecutar pruebas unitarias:  

```bash
pytest -q
```

Incluye pruebas de similitud y validación del filtro.  
Tests relacionados con S3 se saltan automáticamente si no hay credenciales configuradas.  

---

## 📋 Homónimos filtrados (primeras 10 filas de ejemplo)

| original              | homonimo              | score |
|-----------------------|-----------------------|-------|
| Carrera 70 # 26A - 33 | Carrera 70 # 26A - 33 | 100.0 |
| Carrera 70 # 26A - 33 | Carrera 70 # 26A 33   | 100.0 |
| Carrera 70 # 26A - 33 | Carrera 70 26A - 33   | 100.0 |
| Carrera 70 # 26A - 33 | Carrera 70 26A 33     | 100.0 |
| Carrera 70 # 26A - 33 | Carrera 70 No 26A - 33| 100.0 |
| Carrera 70 # 26A - 33 | Carrera 70 No 26A 33  | 100.0 |
| Carrera 70 # 26A - 33 | Carrera 70 Nro 26A - 33|100.0 |
| Carrera 70 # 26A - 33 | Carrera 70 Nro 26A 33 | 100.0 |
| Carrera 70 # 26A - 33 | Carrera 70 Num 26A - 33|100.0 |
| Carrera 70 # 26A - 33 | Carrera 70 Num 26A 33 | 100.0 |

> Nota: el archivo completo `homonimos_filtrados.csv` contiene todas las filas.  

---

## ☁️ Uso con AWS S3
El pipeline también soporta la carga de archivos desde AWS S3 antes de procesarlos.  

Configurar credenciales en PowerShell (solo usuarios finales):  

```powershell
setx AWS_ACCESS_KEY_ID "su_access_key"
setx AWS_SECRET_ACCESS_KEY "su_secret_key"
setx AWS_DEFAULT_REGION "us-east-2"
setx S3_BUCKET "nombre_de_su_bucket"
setx S3_PREFIX "uploads/"
```

Subir archivo de prueba a S3:  

```powershell
aws s3 cp ./sample_data/ejemplo.txt s3://nombre_de_su_bucket/uploads/ejemplo.txt
```

Ejecutar pipeline con S3:  

```bash
python -m app.main run   --inputs ejemplo.txt   --workdir ./workdir/from_s3   --threshold 90   --s3
```

El programa descargará automáticamente el archivo desde S3, lo procesará y generará:  
- `homonimos.csv`, `resultados.csv`, `resultados_unicos.csv`  
- `mapa.html`, `mapa_unicos.html`  
- `resultados.db`  

---

## 👤 Autor
Proyecto desarrollado por [Juan Esteban Cardozo Rivera](https://github.com/JuanC101195)  
Prueba Técnica de Operaciones 2025.  

