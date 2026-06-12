# Cumplimiento del Estándar ISO/IEC 27701:2025 (PIMS)

Este documento establece los lineamientos para el Sistema de Gestión de Información de Privacidad (PIMS) basados en la norma ISO/IEC 27701:2025, extendiendo nuestros controles de ISO 27001/27002 para asegurar la protección de la Información Personalmente Identificable (PII) en OmniVoC SaaS.

## 1. Contexto de la Organización y Roles (Cláusula 4 y 5)
*   **Rol de la Organización:** OmniVoC actúa principalmente como **Procesador de PII** (PII Processor) para nuestros clientes B2B (bancos), pero también asume responsabilidades de **Controlador de PII** (PII Controller) al extraer proactivamente datos de fuentes públicas (redes sociales, tiendas de apps).
*   **Privacidad por Diseño y por Defecto:** La privacidad se integra desde la arquitectura base. La anonimización temprana (Capa Bronze a Silver) garantiza el cumplimiento de PII minimization.

## 2. Controles para el Procesamiento de PII (Anexo A y B)
*   **Minimización y De-identificación de PII (B.1.4.5 y B.1.4.6):** Se garantiza que la PII no necesaria para la extracción de "Sentimiento" o "NPS" (como el nombre de usuario o foto de perfil) se anonimice mediante funciones de un solo sentido (Hashing SHA-256) antes del análisis, impidiendo la re-identificación.
*   **Base Legal para el Procesamiento (B.1.2.3):** Al tratarse de datos públicos de tiendas de aplicaciones, la base legal se sustenta en el interés legítimo y la disponibilidad pública de la información, respetando siempre los términos de servicio (TOS) de las plataformas fuente.
*   **Gestión de Incidentes de Privacidad (B.3.11):** Integrado a nuestra Gestión de Incidentes (ITIL 4). Cualquier evento que comprometa la confidencialidad de la PII scrapeada activará el protocolo de respuesta ante incidentes mayores (*Swarming*) e informará al cliente B2B afectado.

## 3. Registros de Procesamiento de PII (B.1.2.9)
Se mantendrá un registro explícito en nuestros Data Contracts y Data Lakehouse (audit_logs) que documente:
*   Las categorías de PII procesadas.
*   La justificación de la recolección.
*   Las medidas de seguridad organizacionales implementadas (Control de Acceso Lógico a DuckDB).
