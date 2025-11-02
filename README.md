
# Laboratorio MLOps — MLflow

Repositorio del laboratorio de MLOps: uso de MLflow para crear experimentos, registrar métricas/hiperparámetros y versionar modelos localmente.

Objetivo

- Practicar el registro de experimentos y modelos con MLflow. Aprender a ejecutar runs, revisar métricas y publicar modelos en el registro local.

Archivos clave

- `tracking_introduction.py` — script de ejemplo que ejecuta un experimento y lo registra en MLflow.
- `ml_model_registry.py`, `ml_models_registry.py` — utilidades para registrar y versionar modelos.
- `mlruns/` — almacenamiento local de runs, métricas, parámetros y artefactos.

Requisitos mínimos

- Python 3.8+
- `pip`
- Dependencias listadas en `requirements.txt` (incluye `mlflow`).

Instalación (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Uso rápido (pasos del laboratorio)

1) Ejecutar el experimento de ejemplo (registra parámetros, métricas y artefactos):

```powershell
python .\tracking_introduction.py
```

2) Levantar la interfaz web de MLflow para inspeccionar runs y modelos:

```powershell
mlflow ui --backend-store-uri .\mlruns --port 5000
```

Abrir http://127.0.0.1:5000 en el navegador y seleccionar el experimento correspondiente.

Registro de modelos (resumen)

- El script de ejemplo puede llamar a `mlflow.sklearn.log_model()` o `mlflow.register_model()` para almacenar el modelo en `mlruns/` y en `models/` (registro local). Revisa `mlruns/` y `models/` tras ejecutar el script para ver versiones.

Verificación rápida

- Tras ejecutar `tracking_introduction.py`, comprueba que en `mlruns/` aparecen nuevas carpetas con `metrics/`, `params/` y `artifacts/`.
- Abre la UI de MLflow para comprobar métricas, comparar runs y ver modelos versionados.

---

Archivo generado/actualizado por el mantenedor del repositorio: README en español para facilitar uso local con PowerShell y MLflow.
