# Cumplimiento del Estándar ISO 22301:2012 (Continuidad del Negocio)

Este documento condensa los requisitos para el Sistema de Gestión de Continuidad del Negocio (SGCN) aplicables a **OmniVoC SaaS**, extraídos de la norma ISO 22301. Garantiza que nuestro sistema pueda sobrevivir a incidentes disruptivos (caídas de API, corrupción de datos, fallos de infraestructura) y recuperarse en un tiempo aceptable.

## 1. Análisis de Impacto del Negocio (BIA) y Evaluación de Riesgos (Cláusula 8.4)
Para cumplir con este requisito, hemos consolidado el detalle de procesos críticos, RTO (Recovery Time Objective), MTPD (Maximum Tolerable Period of Disruption), así como la matriz de riesgos y mitigaciones en el documento anexo:

👉 **[BUSINESS_IMPACT_ANALYSIS.md](../BUSINESS_PRODUCT/BUSINESS_IMPACT_ANALYSIS.md)**

## 2. Estrategias y Procedimientos de Continuidad (Cláusula 8.4.4 y 8.5)
*   **Backups Cíclicos y Snapshots:** La base de datos local (DuckDB) y la capa Bronze (Parquet) deben tener respaldos automatizados.
*   **Degradación Elegante (Graceful Degradation):** Si el servicio NLP falla, el sistema debe seguir funcionando mostrando métricas descriptivas básicas sin romper el dashboard entero.
*   **Planes de Continuidad del Negocio (BCP):** Procedimientos técnicos claros sobre cómo restaurar el estado de la aplicación desde el último checkpoint exitoso (idempotencia en pipelines).

## 3. Pruebas, Ejercicios y Revisión (Cláusula 8.6 y 9)
*   **Simulacros de Recuperación (Disaster Recovery Tests):** Periodicamente, simular la eliminación de la capa Silver para verificar que el pipeline ELT puede regenerarla completamente desde Bronze en el tiempo esperado.
*   **Auditorías Internas:** Revisiones del SGCN post-incidente documentadas en `AGENT_LOGS.md` para aplicar mejora continua (PDCA - Plan, Do, Check, Act).
