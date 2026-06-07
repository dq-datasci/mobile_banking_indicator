# Product Specifications (Specs-Kit y OpenSpec)

Para mantener la calidad de grado corporativo, toda nueva característica debe seguir esta plantilla de especificación.
Además, nos regimos por el estándar **OpenSpec**: las especificaciones deben ser legibles por humanos y por máquinas (Markdown estricto), garantizando la interoperabilidad con nuestros clientes B2B.

## Plantilla Base de Implementación (Spec)

### 1. Resumen (Pitch)
*¿Qué estamos construyendo y por qué importa?*

### 2. Roles Involucrados
*   **Cloud / DevOps Architect:** Configura la infraestructura y permisos.
*   **Data Engineer:** Construye los pipelines, data contracts y scraping.
*   **MLOps / Data Scientist:** Diseña, entrena y productiviza el modelo (PyCaret, MLflow).
*   **Data Analyst / Econometrista:** Desarrolla los modelos matemáticos causales (Logit, Markov).
*   **UI/UX Engineer:** Construye el dashboard.

### 3. Requerimientos de Datos (Ingesta)
*   *Esquema esperado (Data Contract)*
*   *Privacidad y Anonimización (ISO 27001)*

### 4. Casos de Uso y Flujo (UX)
*   *¿Cómo interactúa el usuario final con esto en el Dashboard?*

### 5. Definición de "Terminado" (DoD)
*   *¿Cuáles son las métricas de éxito? (ej. Precisión del modelo > 85%, Latencia < 200ms).*
