
# Laboratorio MLOps — Registro y tracking con MLflow

Este repositorio contiene ejemplos y utilidades del laboratorio para practicar tracking de experimentos y registro/versionado de modelos usando MLflow (almacenamiento local en `mlruns/` y `models/`).

Contenido principal

- `tracking_introduction.py` — ejemplo de experimentos (incluye scripts para LLMs, registro de métricas, artefactos y registro de modelos).
- `LLM_models_tracking.py` — script de ejemplo que rastrea ejecuciones de LLMs (Gemini / Ollama), registra métricas, artefactos y registra modelos en el Model Registry.
- `ml_model_registry.py` / `ml_models_registry.ipynb` — pipeline de ejemplo (dataset wine) que entrena, evalúa, registra métricas y guarda el modelo con `mlflow.sklearn.log_model()`.
- `resumen_estadisticas.txt`, `gemini_output.txt`, `ollama_output.txt` — ejemplos de artefactos generados por los scripts.
- `mlruns/` — almacenamiento local generado por MLflow (runs, métricas, parámetros, artefactos).

Objetivos del laboratorio

- Aprender a configurar MLflow en local y usar su UI para explorar experimentos.
- Registrar parámetros, métricas y artefactos desde scripts Python.
- Guardar y versionar modelos en el Model Registry local.
- Comparar runs y promover versiones de modelos entre etapas (None → Staging → Production).

Requisitos

- Python 3.8 o superior
- pip
- Dependencias (ver `requirements.txt`)

Instalación rápida (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Nota: `requirements.txt` incluye `mlflow` y librerías comunes de data science (scikit-learn, pandas, numpy, etc.).

Ejecutar los ejemplos

1) Ejecutar el ejemplo de estadísticas (genera métricas y artefactos):

```powershell
python .\tracking_introduction.py
```

Este script registra un experimento de estadísticas y guarda `resumen_estadisticas.txt` como artefacto en `mlruns/`.

2) Entrenar y registrar el modelo de ejemplo (Wine dataset):

```powershell
# Ejecuta el script / notebook que entrena y registra el modelo 'wine_model'
python .\ml_model_registry.py
```

El pipeline entrena un `Pipeline` de scikit-learn (StandardScaler + LogisticRegression), registra parámetros y métricas y llama a `mlflow.sklearn.log_model(pipe, "wine_model", registered_model_name="wine_model")`.

3) Tracking de LLMs y registro de modelos (Gemini / Ollama)

- `LLM_models_tracking.py` y `LLM_models_tracking.py` (o el contenido en `LLM_models_tracking.py`) contienen ejemplos que: configuran providers (Gemini/Ollama), miden latencia/tokens, registran métricas y artefactos (prompts/respuestas) y usan `mlflow.register_model()` para registrar modelos como `llm_gemini_chat` y `llm_ollama_chat`.
- Antes de ejecutar estos scripts asegúrate de tener las credenciales/API keys necesarias en variables de entorno o `.env` (p. ej. `GEMINI_API_KEY`).

4) Levantar la UI de MLflow

```powershell
mlflow ui --backend-store-uri .\mlruns --port 5000
```

Abrir en el navegador: http://127.0.0.1:5000 — podrás explorar experimentos, comparar runs y ver modelos registrados.

Ver modelos y versiones

- Desde la UI puedes ver el Model Registry y las versiones registradas.
- Desde código puedes usar `MlflowClient` para listar versiones y cambiar etapas:

```python
from mlflow.tracking import MlflowClient
client = MlflowClient()
client.transition_model_version_stage(name="wine_model", version=1, stage="Staging")
```

Buenas prácticas y notas

- Mantén un entorno virtual aislado para instalar dependencias.
- Usa `mlflow.set_tracking_uri("http://127.0.0.1:5000")` si trabajas con un servidor MLflow local.
- Cuando registres modelos con `registered_model_name`, MLflow creará entradas en la sección *Models* (Model Registry).
- Revisa `mlruns/` localmente para inspeccionar estructura: cada run contiene `metrics/`, `params/` y `artifacts/`.

Estructura de archivos (resumen)

- `README.md` — este archivo
- `requirements.txt` — dependencias del proyecto
- `tracking_introduction.py` — ejemplo de tracking (estadísticas y/o LLMs según el script)
- `LLM_models_tracking.py` — tracking y registro de LLMs (Gemini/Ollama)
- `ml_model_registry.py` / `ml_models_registry.ipynb` — pipeline de ejemplo (wine) y registro del modelo
- `mlruns/` — carpeta generada por MLflow con todos los runs y artefactos

Problemas comunes

- Si la UI no arranca, revisa que no haya otro proceso usando el puerto 5000.
- Errores al registrar modelos: revisa que `mlflow` esté apuntando al mismo `backend_store_uri` donde se guardan los runs.
- Al usar APIs externas (Gemini, Ollama), valida credenciales y endpoints.

Contribuir

- Para mejoras o correcciones, abre un issue o PR en el repositorio. Incluye pasos para reproducir y cualquier error relevante.

Contacto

- Mantenedor: LeyLopez

---

Archivo regenerado para reflejar el contenido actual del laboratorio: scripts de tracking, ejemplos de registro de modelos y uso de MLflow en local.
