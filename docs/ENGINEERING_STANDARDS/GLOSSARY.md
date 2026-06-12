# Glosario Técnico y de Negocio Corporativo

Este documento define la terminología estándar utilizada a lo largo del proyecto para garantizar que Data Engineers, Econometristas e Inversores hablen el mismo idioma.

## A. Términos de Negocio
*   **BaaS (Banking as a Service):** Modelo de negocio donde vendemos nuestra tecnología (vía API) para que un banco real la integre en su sistema.
*   **Churn / Riesgo de Fuga:** La probabilidad matemática de que un cliente elimine su cuenta bancaria o desinstale la aplicación tras una mala experiencia.
*   **NPS (Net Promoter Score):** KPI de marketing que mide la lealtad. Se calcula agrupando a usuarios en Promotores (5 estrellas), Pasivos (3-4) y Detractores (1-2).
*   **Omnicanalidad:** Estrategia de escuchar al cliente en *todos* los canales disponibles simultáneamente (Redes sociales, Foros, Tiendas de Apps).

## B. Términos de Arquitectura y Data Engineering
*   **Data Lakehouse:** Arquitectura que combina el almacenamiento masivo y barato de un *Data Lake* con las garantías transaccionales (ACID) y estructura de un *Data Warehouse*.
*   **ADR (Architecture Decision Record):** Documento oficial que rastrea qué tecnología decidimos usar y por qué (ej. *Por qué se eligió FastAPI sobre Flask*).
*   **Vertical Slices:** Metodología ágil donde no se construye el software por capas horizontales separadas (primero toda la DB, luego toda la API), sino que se construye una "tajada" funcional de inicio a fin (ej. Scraping + Base de Datos + Dashboard solo para el Login).
*   **Idempotencia:** Propiedad de un script de datos que garantiza que, sin importar si lo ejecutas 1 vez o 1000 veces, el resultado en la base de datos será exactamente el mismo (sin duplicados).
*   **Star Schema (Esquema de Estrella):** Modelo de datos analítico (usado en la capa Gold) donde una tabla central de "Hechos" (métricas) se rodea de tablas de "Dimensiones" (atributos descriptivos) para consultas ultrarrápidas.
*   **SCD Type 2 (Slowly Changing Dimensions):** Técnica de modelado donde, si un atributo cambia (ej. una app cambia de categoría), en lugar de sobrescribir el registro antiguo, se crea una nueva fila con fechas de validez (`valid_from`, `valid_to`), preservando la historia completa.

## C. Términos de Inteligencia Artificial (IA) y MLOps
*   **RAG (Retrieval-Augmented Generation):** Técnica donde se "alimenta" a un LLM (como ChatGPT/LangChain) con datos privados (nuestras reseñas scrapeadas) antes de que responda una pregunta.
*   **LangGraph:** Framework especializado en crear agentes de IA con "estado" (memoria), permitiendo que el chatbot sostenga conversaciones complejas a largo plazo.
*   **MLOps (Machine Learning Operations):** Disciplina que automatiza el entrenamiento, testeo y despliegue de modelos ML a producción usando CI/CD y MLflow.

## D. Términos de Econometría / Modelización
*   **Variable Proxy:** Variable construida artificalmente para aproximar algo que no se puede medir directamente. (Ej. Usar "Sentimiento extremadamente negativo + 1 estrella" como Proxy de que el cliente se fugó).
*   **Modelo Logit (Regresión Logística):** Técnica econométrica de elección discreta que calcula probabilidades entre 0 y 1. Lo usaremos para el Churn.
*   **Cadenas de Markov:** Proceso estocástico (matemático) que calcula la probabilidad de que un cliente transite de un estado (ej. Satisfecho) a otro (ej. Frustrado).

## E. Términos de Gestión de Servicios (ITIL 4)
*   **SVS (Sistema de Valor del Servicio):** Modelo que describe cómo los componentes y actividades de una organización se combinan para crear valor.
*   **Incidente:** Interrupción no planificada o reducción de la calidad de un servicio.
*   **Problema:** Causa o causa potencial de uno o más incidentes.
*   **Error Conocido (Known Error):** Un problema que se ha analizado pero aún no se ha resuelto.
*   **Solución Temporal (Workaround):** Acción que reduce o elimina el impacto de un incidente o problema mientras no está disponible una resolución definitiva.
*   **Mesa de Servicios (Service Desk):** Punto único de contacto entre el proveedor de servicios y todos sus usuarios.
