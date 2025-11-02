'''
Tracking de Modelos de Lenguaje (LLMs)

Objetivo: Aplicar MLflow para rastrear, comparar y registrar ejecuciones de modelos de lenguaje.

Actividades: 
Ejecuta el ejemplo con Gemini (Google) y otro con Ollama local.
Registra: Parámetros: modelo, temperatura, proveedor, tipo de tarea. 
Métricas: latencia, total de tokens, costo estimado. (pueden simular costo por tokens) 
Artefactos: prompts y respuestas generadas. 
Registra cada modelo en el Model Registry como llm_gemini_chat y llm_ollama_chat.

Promueve ambos a Staging y compara las métricas de latencia y costo.


'''
import time
import mlflow
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)


gemini_api_key = os.getenv('GEMINI_API_KEY')


mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("tracking_llm_real")
print("Tracking URI:", mlflow.get_tracking_uri())


#simulacion de costos por tokens
COST_PER_1M_TOKENS = {
    "gemini": {"input": 0.075, "output": 0.30},
    "ollama": {"input": 0.0, "output": 0.0}
}

def calculate_cost(provider, prompt_tokens, completion_tokens):
    """Calcula el costo estimado basado en tokens"""
    rates = COST_PER_1M_TOKENS[provider]
    input_cost = (prompt_tokens / 1_000_000) * rates["input"]
    output_cost = (completion_tokens / 1_000_000) * rates["output"]
    return input_cost + output_cost

'''# Google model '''


# Config Gemini usando el endpoint OpenAI-compatible
gemini = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model_name = "gemini-2.0-flash"
prompt = "¿Qué es la inteligencia artificial?"
temperature = 0.7


with mlflow.start_run(run_name="gemini_tracking") as run:
    # Registrar parámetros
    mlflow.log_params({
        "provider": "google",
        "model_name": model_name,
        "temperature": temperature,
        "task_type": "chat",
        "prompt": prompt
    })

    # Medir latencia
    t0 = time.perf_counter()
    response = gemini.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    latency_ms = (time.perf_counter() - t0) * 1000

    answer = response.choices[0].message.content

    # Tokens
    prompt_tokens = getattr(response.usage, "prompt_tokens", 0)
    completion_tokens = getattr(response.usage, "completion_tokens", 0)
    total_tokens = prompt_tokens + completion_tokens

    # Costo
    cost = calculate_cost("gemini", prompt_tokens, completion_tokens)

    print(answer)
    # Registrar métricas
    mlflow.log_metric("latency_ms", latency_ms)
    mlflow.log_metric("prompt_tokens", prompt_tokens)
    mlflow.log_metric("total_tokens", total_tokens)
    mlflow.log_metric("completion_tokens", completion_tokens)
    mlflow.log_metric("estimated_cost_usd", cost)

    # Guardar la salida como artefacto
    with open("gemini_output.txt", "w", encoding="utf-8") as f:
        f.write(f"Prompt: {prompt}\n\nRespuesta: {answer}")
    mlflow.log_artifact("gemini_output.txt")

    mlflow.register_model(f"runs:/{run.info.run_id}/model", "llm_gemini_chat")

print("✅ GEMINI Model Registered")


''' Ollama '''



ollama = OpenAI(
    api_key="ollama", 
    base_url="http://localhost:11434/v1"
)
model_name_ollama = "llama3.2"
prompt_ollama = "Explica qué es MLflow en una frase."

with mlflow.start_run(run_name="ollama_tracking"):
    mlflow.log_params({
        "provider": "ollama",
        "model_name": model_name_ollama,
        "temperature": 0.0,
        "task_type": "chat",
        "prompt": prompt_ollama
        
    })

    t0 = time.perf_counter()
    response = ollama.chat.completions.create(
        model=model_name_ollama,
        messages=[{"role": "user", "content": prompt_ollama}],
        temperature=0.0,
    )
    latency_ms = (time.perf_counter() - t0) * 1000

    answer = response.choices[0].message.content

    # Tokens
    prompt_tokens = getattr(response.usage, "prompt_tokens", 50)  # Estimado si no hay
    completion_tokens = getattr(response.usage, "completion_tokens", 30)
    total_tokens = prompt_tokens + completion_tokens
    cost = calculate_cost("ollama", prompt_tokens, completion_tokens)

    

    mlflow.log_metric("latency_ms", latency_ms)
    mlflow.log_metric("prompt_tokens", prompt_tokens)
    mlflow.log_metric("total_tokens", total_tokens)
    mlflow.log_metric("completion_tokens", completion_tokens)
    mlflow.log_metric("estimated_cost_usd", cost)


    with open("ollama_output.txt", "w", encoding="utf-8") as f:
        f.write(f"Prompt: {prompt_ollama}\n\nRespuesta: {answer}")
    mlflow.log_artifact("ollama_output.txt")

    mlflow.register_model(f"runs:/{mlflow.active_run().info.run_id}/model", "llm_ollama_chat")

print("✅ OLLAMA Model Registered")



# Para promover ambos modelos a Staging
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Promoviendo Gemini a Staging
gemini_versions = client.search_model_versions("name='llm_gemini_chat'")
if gemini_versions:
    client.transition_model_version_stage(
        name="llm_gemini_chat",
        version=gemini_versions[0].version,
        stage="Staging"
    )
    print("✅ Gemini promovido a Staging")

# Promoviendo Ollama a Staging
ollama_versions = client.search_model_versions("name='llm_ollama_chat'")
if ollama_versions:
    client.transition_model_version_stage(
        name="llm_ollama_chat",
        version=ollama_versions[0].version,
        stage="Staging"
    )
    print("✅ Ollama promovido a Staging")

print("\n Comparación completada.")