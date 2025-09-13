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
- Autor  

---

## 📦 Requisitos
- Python 3.10+  
- Cuenta de Google Cloud con **API Key de Geocoding**  
- (Opcional) AWS S3 configurado si se usa la subida de archivos  

Instalar dependencias:

    pip install -r requirements.txt

Configurar variables de entorno (.env):

    GOOGLE_API_KEY=your_api_key_here
    S3_BUCKET=
    S3_PREFIX=

---

## ▶️ Uso
Ejecutar el pipeline:

    python -m app.main run 
      --inputs .\sample_data\ejemplo.txt 
      --workdir .\workdir 
      --threshold 90

- --inputs: archivo(s) de entrada (PDF o TXT)  
- --workdir: directorio de salida  
- --threshold: umbral de similitud (default 90)  
- --s3: opcional, subir a S3 antes de procesar  

---

## 📂 Archivos generados
En el directorio workdir/ encontrarás:  

- homonimos.csv / .xlsx: lista completa de homónimos  
- homonimos_filtrados.csv / .xlsx: homónimos con score ≥90  
- 
esultados.csv / .xlsx: direcciones geocodificadas  
- 
esultados_unicos.csv / .xlsx: resultados únicos por dirección formateada  
- 
esultados.db: base de datos SQLite con 3 tablas:  
  - homonimos_filtrados  
  - geocoding  
  - geocoding_unicos  
- mapa.html y mapa_unicos.html: mapas interactivos con pines  

---

## 🧪 Validación del filtro
Script incluido: 
alidate_filter.py  

Ejecutar:

    python .\validate_filter.py

Resultado esperado:  
- Los 60 homónimos buenos pasan (score=100).  
- Casos artificiales “malos” (Carrera 71…, Calle 70…, Bogotá…) no pasan (score <90).  

---

## 📊 Ejemplo de salida
    Umbral = 90
    PASARON: 60 de 65
    NO PASARON: 5

    --- Ejemplos que PASAN ---
    [GOOD] Carrera 70 # 26A - 33  -> score=100.0
    [GOOD] Carrera 70 No 26A 33   -> score=100.0

    --- Ejemplos que NO PASAN ---
    [BAD] Av 70 # 26A - 33, Bogota  -> score=83.3

---

## 🗺️ Mapas
Abrir los mapas generados en navegador:

    Start-Process .\workdir\mapa.html
    Start-Process .\workdir\mapa_unicos.html

Cada pin muestra:  
- Dirección formateada  
- Coordenadas (lat, lng)  
- Score de similitud  

---

## 🧪 Tests
Ejecutar pruebas unitarias:

    pytest -q

Incluye pruebas de similitud y validación del filtro.

---

## 📋 Homónimos filtrados (primeras 20 filas)

```text
original                           homonimo                           score
----------------------------------- ----------------------------------- -----
Carrera 70 # 26A - 33              Carrera 70 # 26A - 33               100.0
Carrera 70 # 26A - 33              Carrera 70 # 26A 33                 100.0
Carrera 70 # 26A - 33              Carrera 70 26A - 33                 100.0
Carrera 70 # 26A - 33              Carrera 70 26A 33                   100.0
Carrera 70 # 26A - 33              Carrera 70 No 26A - 33              100.0
Carrera 70 # 26A - 33              Carrera 70 No 26A 33                100.0
Carrera 70 # 26A - 33              Carrera 70 Nro 26A - 33             100.0
Carrera 70 # 26A - 33              Carrera 70 Nro 26A 33               100.0
Carrera 70 # 26A - 33              Carrera 70 Num 26A - 33             100.0
Carrera 70 # 26A - 33              Carrera 70 Num 26A 33               100.0
Carrera 70 # 26A - 33              Carrera 70 Numero 26A - 33          100.0
Carrera 70 # 26A - 33              Carrera 70 Numero 26A 33            100.0
Carrera 70 # 26A - 33              Cr 70 # 26A - 33                    100.0
Carrera 70 # 26A - 33              Cr 70 # 26A 33                      100.0
Carrera 70 # 26A - 33              Cr 70 26A - 33                      100.0
Carrera 70 # 26A - 33              Cr 70 26A 33                        100.0
Carrera 70 # 26A - 33              Cr 70 No 26A - 33                   100.0
Carrera 70 # 26A - 33              Cr 70 No 26A 33                     100.0
Carrera 70 # 26A - 33              Cr 70 Nro 26A - 33                  100.0
Carrera 70 # 26A - 33              Cr 70 Nro 26A 33                    100.0



---

## ☁️ Uso con AWS S3

El pipeline también soporta la carga de archivos desde **AWS S3** antes de procesarlos.

### 🔐 Credenciales
Por motivos de seguridad, **las credenciales de AWS no están incluidas** en este repositorio.  
Para probar el flujo con S3, configure sus propias credenciales en el entorno:

```powershell
# Configurar variables de entorno en PowerShell
setx AWS_ACCESS_KEY_ID "su_access_key"
setx AWS_SECRET_ACCESS_KEY "su_secret_key"
setx AWS_DEFAULT_REGION "us-east-2"
setx S3_BUCKET "nombre_de_su_bucket"
setx S3_PREFIX "uploads/"

---
##📤 Subida de archivos
Subir un archivo de prueba (ejemplo: ejemplo.txt) al bucket en el prefijo configurado:
aws s3 cp .\sample_data\ejemplo.txt s3://nombre_de_su_bucket/uploads/ejemplo.txt

---
##▶ Ejecución del pipeline con S3

Ejecutar el pipeline indicando la opción --s3:

python -m app.main run `
  --inputs ejemplo.txt `
  --workdir .\workdir\from_s3 `
  --threshold 90 `
  --s3


El programa descargará automáticamente el archivo desde S3, lo procesará y generará los artefactos habituales:

homonimos.csv, resultados.csv, resultados_unicos.csv

mapa.html, mapa_unicos.html

resultados.db
---
##👤 Autor
Proyecto desarrollado por **Juan Esteban Cardozo Rivera**  
Prueba Técnica de Operaciones 2025.  
