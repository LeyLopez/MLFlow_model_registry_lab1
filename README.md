
# MLFlow

Este repositorio contiene ejemplos y artefactos de experimentación con MLflow.

## Descripción

Proyecto de ejemplo para registrar experimentos, métricas, parámetros y modelos con MLflow. Incluye scripts y un directorio `mlruns/` con runs y modelos ya registrados localmente.

## Contenido principal

- `tracking_introduction.py` - Script de ejemplo que registra experimentos y métricas en MLflow.
- `ml_model_registry.py` - Utilidades para el registro y gestión de modelos con MLflow.
- `ml_models_registry.py` - Código relacionado con la gestión de versiones de modelos (registro local).
- `resumen_estadisticas.txt` - Artefacto con estadísticas de un experimento de ejemplo.
- `mlruns/` - Carpeta donde MLflow guarda las ejecuciones (runs), métricas, parámetros y modelos.

## Requisitos

Asegúrate de tener Python 3.8+ y `pip` instalados. El archivo `requirements.txt` lista las dependencias necesarias.

## Instalación (PowerShell)

1. Crear y activar un entorno virtual (opcional pero recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

Si tienes problemas con la política de ejecución en PowerShell al activar el entorno, puedes ejecutar:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

## Uso rápido

1. Registrar o reproducir un experimento (ejemplo):

```powershell
python .\tracking_introduction.py
```

Este script registrará parámetros, métricas y (posiblemente) artefactos en la carpeta `mlruns/`.

2. Levantar la interfaz web de MLflow para visualizar runs y modelos:

```powershell
mlflow ui --backend-store-uri .\mlruns --port 5000
```

Abre http://127.0.0.1:5000 en tu navegador.

## Estructura del proyecto

La estructura del repositorio contiene:

- `mlruns/` - almacenamiento local de MLflow. Dentro encontrarás subcarpetas por experimento y runs con `metrics/`, `params/`, `artifacts/` y `tags/`.
- `models/` - (cuando se usa MLflow Model Registry local) versiones de modelos registradas.

## Buenas prácticas

- Mantén el entorno virtual activado cuando trabajes con el proyecto.
- Controla el versionado de tus modelos usando `mlflow.register_model()` cuando quieras publicar versiones en `models/`.
- Añade descripciones claras a tus runs usando tags y `mlflow.set_tag()` para facilitar búsquedas.

## Ejemplos útiles

- Registrar y luego ver la UI:

```powershell
python .\tracking_introduction.py ; mlflow ui --backend-store-uri .\mlruns --port 5000
```

- Activar el entorno y reinstalar dependencias rápidas:

```powershell
.\.venv\Scripts\Activate.ps1 ; pip install -r requirements.txt
```

## Notas finales

Si deseas que añada instrucciones específicas para publicar modelos (por ejemplo en MLflow Tracking Server remoto, o pasos para exportar modelos), dime qué flujo usas (registro local, servidor MLflow, Azure/AWS/GCP) y lo documento.

---

Archivo generado/actualizado por el mantenedor del repositorio: README en español para facilitar uso local con PowerShell y MLflow.
