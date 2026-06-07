# Resumen de Arsenal Analítico (Materias de la Carrera)

Este documento resume las capacidades técnicas y teóricas adquiridas en las materias de la carrera que deben ser implementadas directa o indirectamente en el Indicador Sintético de Banca Móvil.

## 1. Modelización Empresarial II (Econometría Avanzada)
**Profesor:** MSc. Luis Fernando Escobar Caba
**Técnicas Clave a Implementar:**
*   **Series de Tiempo:** Para predecir la evolución de las calificaciones a lo largo de los meses.
*   **Datos de Panel (Multidimensionalidad):** Para comparar la evolución intragrupo (el propio banco a lo largo del tiempo) vs intergrupos (contra los bancos competidores).
*   **Decisiones Discretas (Probit/Logit):** Implementaremos un modelo **Logit** para calcular la probabilidad de que un usuario abandone la app (Churn) basado en características de su reseña (frecuencia de bugs, calificación, sentimiento).
*   **Ecuaciones Simultáneas:** Para modelar cómo la calificación en la App Store afecta las descargas y viceversa (endogeneidad).

## 2. Optimización Empresarial II (Investigación de Operaciones II)
**Técnicas Clave a Implementar:**
*   **Cadenas de Markov (Procesos Estocásticos):** Modelaremos la transición de un cliente de un estado "Satisfecho" a "Frustrado" y finalmente a "Fuga" basado en la secuencia temporal de sus reseñas.
*   **Teoría de Decisiones (Árboles y Bayes):** Para construir un sistema experto en el Dashboard que sugiera a los gerentes bancarios qué feature arreglar primero (ej. "Login" vs "Transferencias") para maximizar el ROI.
*   **Teoría de Colas:** Si integramos reseñas sobre el servicio al cliente, podemos modelar el tiempo de espera y la frustración usando procesos de Poisson.

## 3. Inteligencia Artificial y Machine Learning I
**Técnicas Clave a Implementar:**
*   **Procesamiento de Lenguaje Natural (NLP):** Clasificador de sentimiento y detector de entidades (ej. extraer menciones de "Token", "Biometría", "Caída del sistema") usando LangChain o HuggingFace.

## 4. Ingeniería de Datos
**Herramientas Clave:**
*   **PySpark:** Extracción escalable de reseñas usando `google_play_scraper`.
*   **Databricks / DuckDB:** Almacenamiento Bronze/Silver/Gold.
