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

## 4. Principios SOLID, Clean Code y Vertical Slices
*   **Vertical Slices:** No construimos software en capas aisladas. Cada historia de usuario debe entregar valor de principio a fin (Ej. Scraping -> BD -> Dashboard para un solo caso de uso).
*   **Single Responsibility (SRP)** y **Dependency Inversion (DIP)**. (Ver detalles completos en `SOLID_PRINCIPLES.md`).
*   **Null Safety:** Evitar que los nulos rompan la aplicación ("el null es un mentirosillo").
*   **No "Boolean Traps":** Usar Enums en vez de booleanos mágicos.
*   **Idempotencia y Persistencia:** El procesamiento de datos debe ser idempotente.
*   **Data Contracts:** Obligatorio para el Pipeline de Datos. Definiremos contratos de datos explícitos.
*   **Observabilidad y Resiliencia:** Obligatorio implementar `try/except` robustos y el sistema `logging`. Nada falla silenciosamente.

## 5. Principios Guía de ITIL 4
Para la gestión de los servicios y las operaciones, nos regiremos por los 7 principios de ITIL:
1. **Sitúe el foco en el valor:** Todo lo que hace la organización debe estar orientado al valor.
2. **Comience donde se encuentre:** No empezar de cero; reutilizar lo que ya sirve.
3. **Progrese de forma iterativa mediante la retroalimentación:** Entregas ágiles y constantes.
4. **Colabore y promueva la visibilidad:** Comunicación transparente y trabajo en equipo.
5. **Piense y trabaje holísticamente:** Ningún servicio funciona de forma aislada.
6. **Manténgalo simple y práctico:** Eliminar procesos y métricas sin valor.
7. **Optimice y automatice:** Usar la tecnología para minimizar tareas repetitivas.

## 6. UI/UX y Orquestación Interactiva (CLI)
*   **CLI Hermosa y Amigable:** Implementaremos un menú interactivo en la terminal usando la librería `rich`. Esta será nuestra "Capa 4 de Orquestación". Desde este menú se dispararán las extracciones, entrenamientos ML y el despliegue del Dashboard.
*   **Estética Premium (BI):** El Dashboard en Streamlit debe usar paletas curadas (Premium), sin espacios muertos, y con gráficas 100% legibles (labels, porcentajes y cero errores de layout). Nada de colores básicos.

## 7. Algoritmos y Consistencia (ACID)
*   Medir la eficiencia (Big-O) de las estructuras de datos usadas.
*   Cualquier interacción con Base de Datos debe respetar las transacciones ACID.

## 8. Stack Tecnológico
*   **Entorno:** Micromamba (híbrido R/Python) y Quarto para reportes.
*   **Dashboard:** Streamlit (Integración con Plotly).
*   **Exploración:** DuckDB y ydata_profiling.
*   **Big Data / NLP:** PySpark sobre Databricks.
*   **GenAI / LLMs:** LangChain y LangGraph para flujos conversacionales (RAG).
*   **Tracking de Modelos:** MLflow.

## 9. IA y Pensamiento Crítico
*   Revisar siempre que las sugerencias de la IA tengan sentido lógico y de negocio. Antigravity no debe ejecutar código ciegamente sin evaluar su impacto en la arquitectura.
