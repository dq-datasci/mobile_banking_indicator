# CÓMO TRABAJAMOS (Instrucciones Permanentes para Antigravity)

Este archivo define las reglas arquitectónicas y metodológicas inquebrantables. TODO código escrito por Antigravity debe respetarlas.

## 1. Fecha Límite Inquebrantable
El proyecto DEBE estar finalizado, funcional y empaquetado para su presentación antes del **11 de Junio de 2026**.

## 2. Arquitectura del Sistema (Diseño por Capas)
*   **Capa 4 (Orquestación):** Se debe implementar una capa específica encargada exclusivamente de la orquestación de procesos entre capas. Debe gestionar casos de uso complejos, validación transaccional y errores. NUNCA debe tener lógica de bajo nivel (SQL, scraping).
*   **Interfaces Claras:** Las capas deben comunicarse por interfaces abstractas.

## 3. Patrones de Diseño Obligatorios
*   **Facade:** Para simplificar las llamadas complejas.
*   **Adapter:** Para adaptar las APIs externas (Play Store/App Store).
*   **Strategy:** Excelente para algoritmos intercambiables (Ej: tener un `PlayStoreScraper` y un `AppStoreScraper` que compartan la misma interfaz, o cambiar entre distintos modelos de ML).
*   **Mediator:** Para desacoplar componentes.
*   **Proxy:** Para caché y protección.
*   **Coordinator:** En la Capa 4.

## 4. Principios SOLID y Clean Code
*   **Single Responsibility (SRP)**
*   **Dependency Inversion (DIP):** Depender de abstracciones.
*   **Tell, Don't Ask:** No preguntar por el estado para tomar decisiones externas.
*   **Null Safety:** Evitar que los nulos rompan la aplicación ("el null es un mentirosillo").
*   **No "Boolean Traps":** Usar Enums en vez de booleanos mágicos.
*   **Idempotencia y Persistencia:** El procesamiento de datos (PySpark/Spark) debe ser idempotente. Si se cae a la mitad y se vuelve a correr, debe retomar sin duplicar datos. Usaremos bases locales (`.json`, `DuckDB`) para mantener el estado.
*   **Data Contracts:** Obligatorio para el Pipeline de Datos. Definiremos contratos de datos explícitos (schemas, reglas de calidad y tipos) entre las capas de extracción (Bronze) y limpieza (Silver). Si los datos de Play Store no cumplen el contrato, el pipeline rechaza el lote antes de corromper la BD.

## 5. UI/UX y Orquestación Interactiva (CLI)
*   **CLI Hermosa y Amigable:** Implementaremos un menú interactivo en la terminal usando la librería `rich`. Esta será nuestra "Capa 4 de Orquestación". Desde este menú se dispararán las extracciones, entrenamientos ML y el despliegue del Dashboard.
*   **Estética Premium (BI):** El Dashboard en Streamlit debe usar paletas curadas (Premium), sin espacios muertos, y con gráficas 100% legibles (labels, porcentajes y cero errores de layout). Nada de colores básicos.

## 6. Algoritmos y Consistencia (ACID)
*   Medir la eficiencia (Big-O) de las estructuras de datos usadas.
*   Cualquier interacción con Base de Datos debe respetar las transacciones ACID.

## 7. Stack Tecnológico
*   **Entorno:** Micromamba (híbrido R/Python) y Quarto para reportes.
*   **Dashboard:** Streamlit (Integración con Plotly).
*   **Exploración:** DuckDB y ydata_profiling.
*   **Big Data / NLP:** PySpark sobre Databricks.
*   **GenAI / LLMs:** LangChain y LangGraph para flujos conversacionales (RAG).
*   **Tracking de Modelos:** MLflow.

## 8. IA y Pensamiento Crítico
*   Revisar siempre que las sugerencias de la IA tengan sentido lógico y de negocio. Antigravity no debe ejecutar código ciegamente sin evaluar su impacto en la arquitectura.
