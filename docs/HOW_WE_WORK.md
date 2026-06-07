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
*   **Mediator:** Para desacoplar componentes.
*   **Proxy:** Para caché y protección.
*   **Coordinator:** En la Capa 4.

## 4. Principios SOLID y Clean Code
*   **Single Responsibility (SRP)**
*   **Dependency Inversion (DIP):** Depender de abstracciones.
*   **Tell, Don't Ask:** No preguntar por el estado para tomar decisiones externas.
*   **Null Safety:** Evitar que los nulos rompan la aplicación ("el null es un mentirosillo").
*   **No "Boolean Traps":** Usar Enums en vez de booleanos mágicos.

## 5. Algoritmos y Consistencia (ACID)
*   Medir la eficiencia (Big-O) de las estructuras de datos usadas.
*   Cualquier interacción con Base de Datos debe respetar las transacciones ACID.

## 6. Stack Tecnológico
*   **Entorno:** Micromamba (híbrido R/Python) y Quarto para reportes.
*   **Dashboard:** Streamlit (Integración con Plotly).
*   **Exploración:** DuckDB y ydata_profiling.
*   **Big Data / NLP:** PySpark sobre Databricks.
*   **Tracking:** MLflow.

## 7. IA y Pensamiento Crítico
*   Revisar siempre que las sugerencias de la IA tengan sentido lógico y de negocio. Antigravity no debe ejecutar código ciegamente sin evaluar su impacto en la arquitectura.
