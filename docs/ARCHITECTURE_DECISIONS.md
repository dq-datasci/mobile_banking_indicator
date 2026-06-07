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
