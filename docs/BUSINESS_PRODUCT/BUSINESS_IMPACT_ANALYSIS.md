# Business Impact Analysis (BIA) - OmniVoC SaaS

Este documento forma parte del Sistema de Gestión de Continuidad del Negocio (SGCN) en cumplimiento de la norma **ISO 22301**. Su propósito es identificar los procesos críticos del pipeline de datos, establecer los tiempos máximos tolerables de interrupción, e identificar los riesgos con sus respectivas estrategias mitigantes base.

## 1. Evaluación de Procesos Críticos y Tiempos de Recuperación

| Proceso Crítico | Descripción | Impacto por Interrupción | MTPD (Tiempo Máx. Tolerable) | RTO (Objetivo de Tiempo de Recuperación) |
| :--- | :--- | :--- | :--- | :--- |
| **Ingesta de Datos (Capa Bronze)** | Extracción de reseñas diarias desde AppStore/PlayStore. | **Alto:** Sin datos frescos, el modelo econométrico pierde validez. | 24 Horas | 12 Horas |
| **Orquestación ELT (Capa Silver/Gold)** | Transformación de datos crudos a Star Schema para analítica. | **Medio-Alto:** Retraso en la actualización del Dashboard gerencial. | 24 Horas | 8 Horas |
| **Inferencia de Modelos (NLP)** | Clasificación de sentimiento y extracción de tópicos (HuggingFace). | **Alto:** Imposibilidad de categorizar el feedback no estructurado del cliente. | 12 Horas | 4 Horas |
| **Presentación y Dashboard** | Visualización en Streamlit para la toma de decisiones del banco. | **Crítico:** Pérdida inmediata de valor percibido por el cliente B2B. | 8 Horas | 2 Horas |

## 2. Identificación de Riesgos de Interrupción y Estrategias Mitigantes Base

| Riesgo de Interrupción | Causa Potencial | Estrategia Mitigante Base (Plan de Continuidad) | Nivel de Riesgo Inherente |
| :--- | :--- | :--- | :--- |
| **Bloqueo por Rate-Limiting en APIs** | Exceso de peticiones concurrentes a las tiendas de aplicaciones. | Implementar algoritmo de *Backoff exponencial* y retrasos forzados en el Factory de Scrapers. Uso de tokens de continuación. | Alto |
| **Corrupción de Base de Datos Local** | Falla del disco, reinicio abrupto o escritura concurrente insegura. | Bloqueo lógico (Read-Only/Permisos) desde la Capa de Orquestación hacia la Capa Bronze. (Próximo Sprint: Automatización de respaldos a S3/GCS). | Medio |
| **Fallo en Servicio Cloud de NLP** | Caída del proveedor externo de modelos de Inteligencia Artificial. | **Degradación Elegante:** El sistema orquestador debe ser capaz de saltarse la fase de NLP y continuar operando métricas descriptivas estándar sin colapsar. | Medio |
| **Fuga masiva de PII** | Vulnerabilidad de extracción que captura y almacena nombres/IDs. | Sistema de validación rígida mediante Pydantic que obliga al hashing SHA-256 (Anonimización) antes del ingreso a Bronze. | Bajo (Ya Mitigado) |
