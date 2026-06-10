# Registro de Decisiones Arquitectónicas (ADR)

Este documento registra todas las decisiones tecnológicas y de diseño importantes tomadas a lo largo del proyecto, justificando el *por qué* se eligió una opción sobre las alternativas.

## ADR 001: ELT vs ETL en el Pipeline de Datos
*   **Decisión:** Se utilizará un enfoque **ELT (Extract, Load, Transform)** estructurado en Arquitectura Medallón (Bronze, Silver, Gold), en lugar del tradicional ETL.
*   **Alternativa Rechazada:** ETL clásico (extraer, transformar en memoria y guardar solo el resultado limpio).
*   **Justificación:** Extraeremos las reseñas crudas de la Play Store/App Store y las cargaremos (*Load*) inmediatamente en una capa "Bronze" (usando DuckDB/Parquet local). Las transformaciones (limpieza de texto, modelos NLP) se harán después leyendo esa capa Bronze. Elegimos esto porque las APIs de las tiendas tienen límites de peticiones (*rate-limits*). Si nuestro modelo NLP se equivoca o queremos cambiar las reglas de limpieza, con ELT simplemente reprocesamos los datos crudos almacenados, sin tener que volver a extraer todo de internet.

## ADR 002: Orquestación mediante Menú CLI (Capa 4)
*   **Decisión:** Se utilizará un menú interactivo en consola construido con `rich` para orquestar los procesos.
*   **Alternativa Rechazada:** Ejecutar scripts sueltos (ej. `python extract.py`) o usar orquestadores pesados como Airflow localmente.
*   **Justificación:** Un menú CLI cumple con el requisito estricto de tener una "Capa 4 de Orquestación" clara y encapsulada. Permite a los desarrolladores correr el pipeline completo o por partes sin memorizar comandos, aplicando el patrón *Coordinator*.

## ADR 003: Uso de Streamlit para el Dashboard (Business Intelligence)
*   **Decisión:** Streamlit para la capa de presentación final.
*   **Alternativa Rechazada:** Shiny, Plotly Dash, React/Next.js.
*   **Justificación:** Streamlit ofrece el "Fastest Path to a Live App". Al estar en Python puro, se integra nativamente con nuestros modelos de Machine Learning (NLP) y los gráficos de Plotly sin la sobrecarga de mantener un backend/frontend separado.

## ADR 004: Entorno Híbrido con Micromamba y Quarto
*   **Decisión:** Gestión de dependencias con Micromamba soportando R y Python.
*   **Alternativa Rechazada:** Pip/Venv nativo de Python.
*   **Justificación:** El proyecto requiere modelos de Econometría II (usualmente mejores en R o requieren librerías estadísticas pesadas) e IA/NLP (exclusivo de Python). Micromamba permite aislar ambos lenguajes en un solo entorno de forma extremadamente rápida. Quarto nos permite crear reportes que ejecuten celdas de ambos lenguajes.

## ADR 005: Patrón Strategy y Data Contracts
*   **Decisión:** Implementar Data Contracts entre capas y el patrón Strategy para los extractores.
*   **Justificación:** Cumplimiento de Principios SOLID. Si mañana se quiere agregar una nueva fuente (ej. reseñas de Facebook), solo se añade una nueva *Strategy* sin tocar la orquestación. Los *Data Contracts* aseguran que ninguna basura de la red ensucie la base de datos de análisis.

## ADR 006: Monolito Modular vs Microservicios
*   **Decisión:** El proyecto se construirá como un **Monolito Modular** (todo el código en un solo repositorio estructurado por carpetas).
*   **Alternativa Rechazada:** Microservicios, Kubernetes.
*   **Justificación:** Para un proyecto de Ciencia de Datos / BI, usar Microservicios y Kubernetes es una sobreingeniería masiva (overkill) que solo añadiría latencia de red y costos de servidor. Al usar un Monolito "Modular" (gracias a nuestras capas `src/core`, `src/use_cases`), mantenemos la simplicidad de un solo código base, pero con la limpieza y desacoplamiento como si fueran microservicios. 

## ADR 007: Docker y Estrategia de Despliegue (Web vs Desktop/Mobile)
*   **Decisión:** El producto final se "dockerizará" (Docker) para ser desplegado en la **Web** (Nube).
*   **Alternativas Rechazadas:** App para celular, App de Escritorio nativa.
*   **Justificación:** El objetivo final es un Dashboard Analítico (Indicador Sintético). Visualizar gráficos econométricos complejos y tablas PySpark en la pantalla de un celular brinda una pésima experiencia de usuario. Empaquetarlo como app de escritorio es limitante. Usaremos **Docker** para encapsular nuestro entorno y desplegaremos la aplicación web en la nube (ej. Streamlit Cloud o AWS) para que cualquier profesor o jurado pueda interactuar con el proyecto simplemente usando un link en su navegador.

## ADR 008: Arquitectura de Agentes IA (LangChain y LangGraph)
*   **Decisión:** Mantendremos LangChain y LangGraph como el cerebro lógico para el procesamiento avanzado y agentes RAG.
*   **Justificación:** El RAG nos permitirá "chatear con las quejas de los usuarios". LangGraph nos permite construir agentes con estado persistente. Para este proyecto, el módulo LangChain servirá de soporte para el análisis NLP complejo y la interrogación de los contratos de datos.

## ADR 009: Principios UX/UI del Dashboard (Patrón F y Storytelling)
*   **Decisión:** El Dashboard se diseñará usando el **Patrón F**, Jerarquía Visual estricta, un *Grid System* y la técnica de *Storytelling*.
*   **Alternativas Rechazadas:** Dashboard de "tablero caótico" sin flujo de lectura (ej. Z-Pattern).
*   **Justificación:** Los ejecutivos no leen, escanean. El **Patrón F** dicta que lo más crítico va arriba a la izquierda y el contenido fluye hacia abajo. Usaremos **Storytelling** para responder en secuencia: ¿Qué pasó? (Métricas generales), ¿Por qué pasó? (Modelos NLP causales), ¿Qué debemos hacer? (Árboles de Decisión y Optimización).

## ADR 010: Patrón Singleton para Base de Datos y Pydantic Data Contracts
*   **Decisión:** Se utilizará el patrón Singleton para mantener una única conexión global a DuckDB y `pydantic` para validar estrictamente los datos antes de insertarlos.
*   **Justificación:** Instanciar múltiples veces DuckDB genera bloqueos y sobrecarga de memoria. El Singleton asegura eficiencia (SRP). Pydantic garantiza que la "basura" o cambios inesperados en las APIs de scraping no rompan ni corrompan el Data Lakehouse (Bronze Layer).

## ADR 011: Anonimización de PII en la Capa de Ingesta (Privacy by Design)
*   **Decisión:** Se utilizarán validadores integrados (`@field_validator` de Pydantic) en los *Data Contracts* (ej. `PlayStoreReviewContract`) para aplicar hashing SHA-256 de forma inmediata a los datos personales (PII) durante la instanciación.
*   **Alternativas Rechazadas:** Extraer en texto plano hacia la capa Bronze y luego anonimizar usando PySpark/DuckDB antes de pasar a la capa Silver.
*   **Justificación:** Aplicar *Privacy by Design* garantiza que la base de datos local (capa Bronze) nunca almacene texto plano. Esto mitiga radicalmente el riesgo de fuga de datos en entornos de desarrollo local y cumple de manera más estricta con ISO 27001 y PoLP.
