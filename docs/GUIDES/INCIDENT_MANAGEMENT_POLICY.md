# Política de Gestión de Incidentes y Mesa de Servicios (Service Desk)

Este documento rige el comportamiento de DevOps y soporte técnico ante fallas del sistema, asegurando la continuidad del negocio y el cumplimiento de **ITIL 4**, **ISO 22301** (MTPD) e **ISO 27001** (A.5.24).

## 1. Definición de la Práctica (Mesa de Servicios)
La Mesa de Servicios (Service Desk) actúa como punto único de contacto. En el contexto automatizado de OmniVoC, el `IncidentManager` actúa como el primer nivel de detección (*Tier 1*), enrutando las anomalías del pipeline hacia los canales de los ingenieros DevOps.

## 2. Clasificación de Incidentes
Los incidentes reportados por el `AuditLogger` se clasifican en:
*   **WARNING (Menor):** Fallos no bloqueantes (ej. un rate-limit temporal que aplicó backoff exponencial). No requiere intervención inmediata.
*   **ERROR (Mayor):** Interrupción de un servicio crítico (ej. base de datos inaccesible, API de origen bloqueada permanentemente). Activa el protocolo de **Swarming**.
*   **CRITICAL (Crítico/Seguridad):** Posible fuga de PII, inyección SQL o caída total del Lakehouse. Requiere movilización inmediata del Cloud Architect y DevOps.

## 3. Protocolo de Swarming para Incidentes Mayores
Frente a un incidente Mayor o Crítico, el equipo de soporte no escala jerárquicamente a través de niveles (Tier 1 -> Tier 2 -> Tier 3), sino que aplica **Swarming**: un grupo multidisciplinario (Data Engineer, DevOps y Security) se reúne inmediatamente para diagnosticar y aislar la falla de forma colaborativa, minimizando el RTO.

## 4. Habilitación del Cambio y Errores Conocidos (Problem Management)
*   Si un incidente recurrente no puede resolverse definitivamente, se registra en el repositorio como un **Error Conocido** con un **Workaround** documentado (ej. saltar el scraper de una fuente específica).
*   La resolución estructural de incidentes debe inyectarse a través del pipeline de CI/CD como un Cambio Normal, pasando por todas las aserciones de `pytest`.
