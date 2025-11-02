import mlflow
import numpy as np
from datetime import datetime
import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")



def calcular_estadisticas(datos):
    return {
        'promedio': np.mean(datos),
        'mediana': np.median(datos),
        'desviacion': np.std(datos),
        'minimo': np.min(datos),
        'maximo': np.max(datos)
    }

with mlflow.start_run(run_name="modelo_estadisticas"):
    datos = np.random.normal(loc=50, scale=10, size=1000)
    
    mlflow.log_param("distribucion", "normal")
    mlflow.log_param("media", 50)
    mlflow.log_param("desv_std", 10)
    mlflow.log_param("n_samples", 1000)
    
    stats = calcular_estadisticas(datos)
    
    
    for nombre, valor in stats.items():
        mlflow.log_metric(nombre, valor)
    
    
    with open("resumen_estadisticas.txt", "w") as f:
        f.write("Resumen de Estadísticas\n")
        f.write("=" * 40 + "\n")
        for nombre, valor in stats.items():
            f.write(f"{nombre.capitalize()}: {valor:.4f}\n")
        f.write(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    mlflow.log_artifact("resumen_estadisticas.txt")
    
    
    mlflow.set_tag("tipo", "estadisticas_descriptivas")
    mlflow.set_tag("version", "1.0")
    
    print("Modelo de estadísticas registrado")
    print(f"Promedio calculado: {stats['promedio']:.2f}")
