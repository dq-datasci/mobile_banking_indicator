# Patrones de Diseño Gof Aplicados

Para evitar la deuda técnica y el código espagueti en un proyecto escalable B2B, adoptamos los siguientes patrones de diseño recomendados por la industria (Gang of Four).

## Patrones Creacionales

### 1. Factory Method
*   **Problema:** Necesitamos instanciar múltiples scrapers (Tiktok, Twitter, PlayStore) pero el usuario final o el Menú CLI solo elige una opción en la pantalla.
*   **Solución:** Una clase `ScraperFactory` que recibe un string `"twitter"` y devuelve automáticamente la instancia correcta lista para trabajar, ocultando la complejidad de instanciación.

### 2. Singleton
*   **Problema:** Inicializar la base de datos embebida (DuckDB) o conectar a Databricks múltiples veces consume muchísima RAM.
*   **Solución:** El `DatabaseConnector` se implementará como Singleton. Garantizamos que solo exista una única instancia de conexión activa en todo el ciclo de vida de la app.

## Patrones Estructurales

### 3. Facade
*   **Problema:** Hacer un pipeline de NLP requiere inicializar Tokenizers, cargar embeddings, limpiar caracteres, y llamar al modelo HuggingFace. El desarrollador de Backend se ahogaría importando 20 cosas.
*   **Solución:** Una clase `NLPFacade` que exponga un único método simple: `analyze_text(text)`. Toda la complejidad interna queda oculta tras esta "fachada".

### 4. Adapter
*   **Problema:** La librería nativa de `google_play_scraper` devuelve diccionarios anidados complejos, mientras que nuestra capa Silver espera DataFrames planos.
*   **Solución:** Crearemos adaptadores que envuelvan las respuestas de las APIs externas para que coincidan con nuestros *Data Contracts* internos.

## Patrones de Comportamiento

### 5. Strategy
*   **Problema:** La PlayStore se scrapea usando HTML puro, pero Twitter requiere una API oficial, y Reddit requiere paginación JSON. La lógica cambia drásticamente.
*   **Solución:** El patrón Strategy nos permite inyectar el algoritmo (estrategia) de extracción correcto en tiempo de ejecución, dependiendo de la fuente seleccionada.

### 6. Observer
*   **Problema:** Queremos un sistema de alertas automatizado. Cuando el "Riesgo de Churn" general del banco supera el 15%, debemos enviar un email.
*   **Solución:** El Pipeline de Datos (Sujeto) notificará automáticamente a múltiples Observadores (Módulo de Email, Dashboard Log) cada vez que termine de correr el modelo Logit, de forma totalmente asíncrona.
