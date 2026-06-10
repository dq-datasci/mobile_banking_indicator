# Políticas de DevOps, MLOps y Seguridad

Dado nuestro enfoque Enterprise y B2B, este documento rige las operaciones de infraestructura, despliegue de machine learning y cumplimiento normativo.

## 1. Seguridad Informática y Cumplimiento (ISO 27001)
*   **Principle of Least Privilege (PoLP):** Ningún rol, sistema o base de datos tendrá más permisos de los estrictamente necesarios.
*   **Private Subnets:** La base de datos (DuckDB/Lakehouse) vivirá en una red aislada sin acceso a internet público. Solo la capa de backend (FastAPI/Streamlit) podrá conectarse a ella mediante puertos encriptados.
*   **Anonimización de Datos (PII):** Es estrictamente **ilegal** dentro de este proyecto almacenar nombres de usuario de las redes sociales en texto plano en la capa Silver/Gold. Todo dato personal (PII) en la capa Bronze debe ser hasheado (ej. usando SHA-256) antes del análisis.

## 2. Infraestructura como Código (IaC) y DevOps
*   **Terraform:** Toda la infraestructura en la nube (ej. instancias en Ubicloud, buckets en AWS) se definirá mediante código usando Terraform, eliminando la creación manual de recursos.
*   **CI/CD (Integración y Despliegue Continuo):** Se usarán GitHub Actions. No se permite el despliegue directo a producción (`main`). Todo código debe pasar por Pruebas Unitarias automáticas en `develop`.

## 3. MLOps (Operaciones de Machine Learning)
*   **Trazabilidad con MLflow:** Todos los experimentos, parámetros y métricas de los modelos (PyCaret, Transformers) deben registrarse usando MLflow. Nunca "perderemos" un modelo bueno porque no recordamos qué hiperparámetros usamos.
*   **AutoML con PyCaret:** Para la selección inicial de algoritmos, usaremos PyCaret para comparar rápidamente múltiples baselines estadísticos antes de hacer tuning profundo.

## 4. Observabilidad y Resiliencia
*   **Manejo de Errores (Error Handling):** Todos los scrapers usarán bloques `try/except` rigurosos. Si una red social falla o bloquea nuestra IP, el script no debe romperse; debe atrapar el error, registrar un **Log** estructurado y reintentar con *Backoff Exponencial* (Retrys/Fault Tolerance).
*   **Monitoreo (Logging):** Se usará el módulo nativo de `logging` en Python, configurado para escribir a consola y a archivos de registro, permitiendo auditorías rápidas.
