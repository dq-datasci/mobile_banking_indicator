# Registro de Actividad de Agentes (Agent Logs)

Este archivo es el registro de actividades de Antigravity.
**REGLA:** Antes de hacer commit o terminar una sesión, el agente DEBE agregar una entrada aquí con la fecha, quién ejecutó, qué se hizo y qué sigue.

---

### [2026-06-06] - Inicialización del Proyecto 
*   **Estado:** Se creó la estructura del repositorio y se inicializó Git en la rama `develop`.
*   **Hecho:** Se definieron las reglas de arquitectura, el manual `README.md`, el Kanban ajustado a la fecha límite del 11 de Junio, y se importó el resumen base (contexto).
*   **Siguiente paso:** Crear el entorno Micromamba, e iniciar el Sprint 1 (Extracción de datos con PySpark).

---

### [2026-06-08] - Sprint 1: Factory de Scrapers y Entorno 
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `environment.yml`, `src/core/interfaces/scraper_interface.py`, `src/infrastructure/extractors/scraper_factory.py`, `playstore_scraper.py`, `appstore_scraper.py`.
*   **Hecho:** Se creó el entorno `omnivoc_env` con micromamba. Se implementó el patrón Factory Method asegurando LSP para la extracción. Se comprobó la conexión a Play Store guardando las reseñas puras en formato Parquet en la capa Bronze.
*   **Siguiente paso:** Debemos abordar la Historia 1.2.1 (Singleton Database y Data Contracts para DuckDB) y la 1.2.2 (Pipeline de Anonimización).

---

### [2026-06-10] - Cierre Historia 1.1.1 y Corrección de LSP 
*   **Estado:** Se revisó el código en la rama `feature/1.1.1-scrapers-factory`.
*   **Hecho:** Se añadió el método `save_to_bronze` a la interfaz base `BaseScraper` para cumplir con el Principio de Sustitución de Liskov (LSP). Se actualizaron KANBAN y USER_STORY_MAP para marcar la Historia 1.1.1 como finalizada.
*   **Siguiente paso:** Crear un Pull Request de `feature/1.1.1-scrapers-factory` hacia `develop`, hacer merge y comenzar con la Historia 1.2.1 (Singleton Database y Data Contracts).

---

### [2026-06-10] - Mantenimiento de Repositorio y Mejora de Prompts 
*   **Estado:** Sincronización y mantenimiento en la rama `develop`.
*   **Hecho:** Se resolvieron dudas sobre conflictos de Git y se limpiaron las ramas fusionadas (`chore/remove-context-materials` y `feature/1.1.1-scrapers-factory`). Además, se robustecieron los prompts del `README.md` para garantizar el control estricto del progreso ágil en futuras sesiones.
*   **Siguiente paso:** Crear la rama `feature/1.2.1-singleton-database` e iniciar el desarrollo de la Historia 1.2.1 bajo el rol de Cloud Architect .

---

### [2026-06-10] - Historia 1.2.1: Singleton Database y Data Contracts 
*   **Estado:** Completado en la rama `feature/1.2.1-singleton-database`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `src/core/contracts/review_contract.py`, `src/core/interfaces/database_interface.py`, `src/infrastructure/database/duckdb_singleton.py`, `environment.yml`.
*   **Hecho:** Se implementaron Pydantic Data Contracts para validar el esquema de datos. Se creó la interfaz `IDatabase` cumpliendo el principio DIP. Se implementó `DuckDBConnection` usando el patrón Singleton para prevenir sobrecarga de RAM. Se actualizaron las dependencias y se verificó todo exitosamente. También se agregó el ADR 010.
*   **Siguiente paso:** Hacer Pull Request a `develop` de la rama actual y, posteriormente, iniciar la Historia 1.2.2 (Pipeline de Anonimización ISO 27001) asignada al rol de Data Engineer.

---

### [2026-06-10] - Historia 1.2.2: Pipeline de Anonimización ISO 27001 
*   **Estado:** Completado en la rama `feature/1.2.2-anonimizacion-pipeline`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `src/core/security/anonymizer.py`, `src/core/contracts/review_contract.py`, `tests/test_anonymizer.py`, `environment.yml`.
*   **Hecho:** Se implementó `PIIAnonymizer` con hashing SHA-256 y se inyectó en el `PlayStoreReviewContract` como un validador de Pydantic. Ahora la PII se enmascara antes de tocar la BD Bronze (Privacy by Design). Las pruebas unitarias fueron exitosas (5/5).
*   **Siguiente paso:** Hacer Pull Request a `develop` e iniciar la Historia 1.3.1 (CI/CD GitHub Actions y Pre-commits) asignada al rol de DevOps (David).

---

### [2026-06-10] - Actualización de Arquitectura ADR 011 
*   **Estado:** Modificación de Documentación en la rama `feature/1.2.2-anonimizacion-pipeline`.
*   **Hecho:** Se agregó el **ADR 011** a `ARCHITECTURE_DECISIONS.md` para asentar formalmente la decisión de aplicar "Privacy by Design" y realizar la anonimización de PII al nivel del *Data Contract* en lugar de hacerlo en pipelines asíncronos ELT.
*   **Siguiente paso:** Terminar sesión y enviar Pull Request.

---

### [2026-06-10] - Historia 1.3.1: CI/CD GitHub Actions y Pre-commits 
*   **Estado:** Completado en la rama `feature/1.3.1-ci-cd-precommits`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `environment.yml`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml`, `docs/ADRs/ARCHITECTURE_DECISIONS.md`, `README.md`.
*   **Hecho:** Se implementaron los pipelines de CI/CD mediante GitHub Actions. Se instaló `ruff` y `pre-commit` para aplicar formateo y linting estricto automático, reemplazando a Flake8 y Black (aprobado mediante ADR 012). Adicionalmente, se configuró el repositorio remoto para utilizar `develop` como rama por defecto, y se automatizó la creación y eliminación de Pull Requests desde la terminal en el `README.md`.
*   **Siguiente paso:** Cambiar al rol de Data Analyst (David) e iniciar la Historia 2.1.1 (Análisis Exploratorio ydata-profiling).

---

### [2026-06-11] - Documentación de Arquitectura de Datos y Schemas 
*   **Estado:** Completado en la rama `feature/1.4-data-architecture-schemas`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `docs/ENGINEERING_STANDARDS/DATA_ARCHITECTURE.md`, `docs/SCRUM/KANBAN.md`, `docs/SCRUM/USER_STORY_MAP.md`, `docs/ENGINEERING_STANDARDS/GLOSSARY.md`.
*   **Hecho:** Se formalizó la arquitectura de datos ELT (Medallón) con diagramas Mermaid conceptuales y lógicos. Se definió el Star Schema para la capa Gold incorporando Dimensiones Lentamente Cambiantes (SCD Tipo 2). Se incluyeron las Historias 1.4.1 (Pipeline Silver) y 1.4.2 (Pipeline Gold) explícitamente en el Kanban y Story Map. Se actualizó el Glosario.
*   **Siguiente paso:** Crear el Pull Request, fusionar a `develop` e iniciar la Historia 2.1.1 (Análisis Exploratorio ydata-profiling).

---

### [2026-06-11] - Cierre de Sesión y Actualización de Arquitectura 
*   **Estado:** Finalización de sesión en la rama `chore/end-of-session-june-11`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `docs/ADRs/ARCHITECTURE_DECISIONS.md`.
*   **Hecho:** Se verificó el cumplimiento de SOLID, Clean Code y principios de seguridad. Se agregó el **ADR 014** para asentar formalmente la decisión de usar Star Schema y SCD Tipo 2 en la capa Gold. El tablero KANBAN y User Story Map fueron actualizados con los últimos movimientos de historias de usuario.
*   **Siguiente paso:** Iniciar la Historia 2.1.1 (Análisis Exploratorio ydata-profiling) en la próxima sesión.

---

### [2026-06-12] - Historia 1.4.1 y 1.4.2: ISO 27002 y Pipeline Silver (Antigravity / Data Engineer)
*   **Estado:** Completado en la rama `feature/1.4.1-pipeline-silver`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `docs/ENGINEERING_STANDARDS/ISO_27002_COMPLIANCE.md`, `docs/ENGINEERING_STANDARDS/DEVOPS_MLOPS_SECURITY.md`, `docs/SCRUM/KANBAN.md`, `docs/SCRUM/USER_STORY_MAP.md`, `src/core/interfaces/data_quality_interface.py`, `src/core/quality/silver_quality_checker.py`, `src/infrastructure/pipelines/silver_pipeline.py`, `tests/test_silver_pipeline.py`.
*   **Hecho:** Se reordenaron las historias y se redactó el cumplimiento de la ISO 27002. Se implementó el Pipeline de la capa Silver junto a su interfaz y chequeo de calidad que verifica el correcto Data Masking de PII y la eliminación de valores nulos o fuera de rango. Se realizaron pruebas automatizadas satisfactorias.
*   **Siguiente paso:** Iniciar la Historia 1.4.3 (Construcción de Capa Gold - Star Schema y SCD Type 2).
### [2026-06-12] - Historia 1.4.3: Capa Gold y SCD Type 2 (David / Data Engineer)
*   **Estado:** Completado en la rama `feature/1.4.3-gold-layer-star-schema`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `src/core/contracts/gold_contracts.py`, `src/infrastructure/pipelines/gold_pipeline.py`, `tests/test_gold_pipeline.py`, documentación (ISO 27001).
*   **Hecho:** Se implementaron los contratos Pydantic para el Star Schema y la clase GoldPipeline. Se verificó el funcionamiento de Slowly Changing Dimensions (Tipo 2) para la dimensión de aplicación y las Surrogate Keys en la tabla de hechos Fact_Reviews. También se agregó la política de cumplimiento de la ISO 27001 y se limpió el repositorio unificando los perfiles de autoría en uno solo (David).
*   **Siguiente paso:** Iniciar la Historia 1.5.1 (Auditoría ISMS y Prevención de Fugas de Datos) según el orden del Kanban.

---

### [2026-06-12] - Historia 1.6.1: Documentación e Implementación del SVS de ITIL 4 (David / Cloud Architect)
*   **Estado:** Completado en la rama `feature/1.4.4-itil-integration`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `docs/ENGINEERING_STANDARDS/ITIL_4_COMPLIANCE.md`, `docs/SCRUM/KANBAN.md`, `docs/SCRUM/USER_STORY_MAP.md`, `docs/ENGINEERING_STANDARDS/GLOSSARY.md`, `docs/GUIDES/HOW_WE_WORK.md`, `docs/ADRs/ARCHITECTURE_DECISIONS.md`.
*   **Hecho:** Se analizó el documento ITIL 4 Foundation y se extrajeron las mejores prácticas aplicables a la arquitectura SaaS. Se documentó el Sistema de Valor del Servicio (SVS), las 4 Dimensiones, los 7 Principios Guía y prácticas como la Mesa de Servicios, Gestión de Incidentes, Problemas y Mejora Continua. Se incluyó el ADR 015 y se agregaron historias al Kanban. Se eliminó el PDF original de ITIL.
*   **Siguiente paso:** Iniciar la Historia 1.6.2 (Definición de Procesos para Mesa de Servicios y Gestión de Incidentes).

---

### [2026-06-12] - Cierre de Sesión (David / Cloud Architect)
*   **Estado:** Limpieza de repositorio y revisión final completada en rama `chore/session-wrapup`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `docs/AGENT_LOGS.md`
*   **Hecho:** Se verificó la integridad de los principios SOLID, DevOps, ISO y ITIL. No se identificaron vulnerabilidades ni desviaciones arquitectónicas. Todas las actividades de reestructuración para la sección 1.5 se completaron satisfactoriamente.
*   **Siguiente paso:** Iniciar la Historia 1.5.2 (Auditoría ISMS y Prevención de Fugas de Datos).

---

### [2026-06-12] - Historia 1.5.2 y 1.5.6: Auditoría ISMS y BIA Inicial ISO 22301 (David / Cloud Architect)
*   **Estado:** Completado en la rama `feature/1.5.2-isms-and-iso22301`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `src/core/security/audit_logger.py`, `src/infrastructure/extractors/scraper_factory.py`, `src/core/interfaces/scraper_interface.py`, `src/infrastructure/extractors/playstore_scraper.py`, `src/infrastructure/extractors/appstore_scraper.py`, `src/infrastructure/database/duckdb_singleton.py`, `docs/ADRs/ARCHITECTURE_DECISIONS.md`, `docs/SCRUM/USER_STORY_MAP.md`, `docs/SCRUM/KANBAN.md`, `docs/ENGINEERING_STANDARDS/ISO_22301_COMPLIANCE.md`.
*   **Hecho:** Se implementó el `AuditLogger` centralizado basado en la librería `logging` como Singleton para cumplir con los controles de ISO 27001 (A.8.15 y A.8.16). Se inyectó el logger en los scrapers de PlayStore y AppStore. Se implementó una barrera de seguridad en `duckdb_singleton.py` para bloquear cualquier escritura no autorizada en la capa Bronze. Se redactó el documento base de cumplimiento ISO 22301, extrayendo los lineamientos del PDF original (el cual fue borrado), y se crearon los ADRs 016 y 017 correspondientes a estas decisiones y al BIA.
*   **Siguiente paso:** Iniciar la Historia 1.5.3 (Procesos de Mesa de Servicios y Gestión de Incidentes).

---

### [2026-06-12] - Actualización de Prompts de Sesión (Antigravity)
*   **Estado:** Completado en la rama `chore/readme-prompt-update`.
*   **Archivos Modificados:** `README.md`, `docs/AGENT_LOGS.md`.
*   **Hecho:** Se actualizó el archivo `README.md` incorporando la exigencia estricta de verificar el documento `BUSINESS_IMPACT_ANALYSIS.md` tanto al inicio como al final de cada sesión. Esto endurece y formaliza las políticas de Continuidad del Negocio (ISO 22301).
*   **Siguiente paso:** Iniciar la Historia 1.5.3 (Procesos de Mesa de Servicios y Gestión de Incidentes) en la próxima sesión.

---

### [2026-06-12] - Historia 1.5.3 y 1.5.7: Incident Management y PIMS (ISO 27701)
*   **Estado:** Completado en la rama `feature/1.5.3-incident-management`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `docs/GUIDES/INCIDENT_MANAGEMENT_POLICY.md`, `src/core/security/incident_manager.py`, `src/core/security/audit_logger.py`, `tests/test_incident_manager.py`, `docs/ENGINEERING_STANDARDS/ISO_27701_COMPLIANCE.md`, `docs/SCRUM/KANBAN.md`, `docs/SCRUM/USER_STORY_MAP.md`.
*   **Hecho:** Se extrajo el contenido de ISO 27701 (PIMS) y se establecieron los roles de Processor/Controller. Se definió la política de Mesa de Servicios e Incidentes Mayores (Swarming) cumpliendo ITIL 4 e ISO 22301. Se implementó el `IncidentManager` con el patrón Observer conectado al `AuditLogger` para detonar alertas críticas, cumpliendo con SOLID y la seguridad esperada.
*   **Siguiente paso:** Iniciar la Historia 1.5.4 (Gestión de Problemas y Habilitación del Cambio en CI/CD).

---

### [2026-06-12] - Cierre de Sesión y Mantenimiento de ISO 27701
*   **Estado:** Completado en la rama `chore/session-wrapup-june-12`.
*   **Archivos Modificados:** `README.md`, `docs/SCRUM/USER_STORY_MAP.md`, `docs/AGENT_LOGS.md`.
*   **Hecho:** Se completaron los criterios de aceptación de la Historia 1.5.7 validando las políticas en el entorno, y se actualizó manualmente el archivo README con el requerimiento de validar la normativa ISO 27701 en cada plan. 
*   **Siguiente paso:** Iniciar la Historia 1.5.4 (Gestión de Problemas y Habilitación del Cambio en CI/CD) en la próxima sesión.

---

### [2026-06-12] - Historia 1.5.4 e ISO 25010: Gestión de Problemas (David / DevOps)
*   **Estado:** Completado en la rama `feature/1.5.4-problem-change-management`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `docs/ENGINEERING_STANDARDS/ISO_25010_COMPLIANCE.md`, `docs/GUIDES/KNOWN_ERRORS.md`, `docs/SCRUM/KANBAN.md`, `docs/SCRUM/USER_STORY_MAP.md`, `docs/ENGINEERING_STANDARDS/GLOSSARY.md`.
*   **Hecho:** Se analizó el estándar ISO 25010 y se documentó su cumplimiento en la arquitectura de datos y microservicios. Se crearon historias asociadas a DevOps y despliegue (Canary, Blue-Green, Rolling Updates). Se implementó el archivo `KNOWN_ERRORS.md` oficializando el flujo de Habilitación del Cambio según ITIL 4.
*   **Siguiente paso:** Iniciar la Historia 1.5.5 (Secure Development Life Cycle y Pruebas de Seguridad).

---

### [2026-06-12] - Historia 1.5.5 e Integración OWASP Top 10 2025 (Antigravity)
*   **Estado:** Completado en la rama `feature/1.5.5-secure-development-lifecycle`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `docs/ENGINEERING_STANDARDS/OWASP_TOP_10_2025_COMPLIANCE.md` (creado), `docs/CONTEXT/202512 - OWASP Top 10 2025 by Miglen Evlogiev.pdf` (eliminado), `docs/SCRUM/KANBAN.md`, `docs/SCRUM/USER_STORY_MAP.md`, `.github/workflows/ci.yml`.
*   **Hecho:** Se destiló el PDF con OWASP Top 10 2025 en un nuevo estándar markdown para prevenir vulnerabilidades A01-A10. Se borró el PDF original. Se añadieron nuevas historias al Scrum para abordar Fallas en la Cadena de Suministro y controles de Acceso/Logging en futuros Sprints. Se completó la Historia 1.5.5 implementando linter de seguridad `bandit` y escáner de secretos `gitleaks` en el pipeline de CI/CD mediante GitHub Actions.
*   **Siguiente paso:** Iniciar la Historia 1.5.10 (Control de Software Supply Chain Failures).

---

### [2026-06-12] - Cierre de Sesión y Mantenimiento de Prompts (Antigravity)
*   **Estado:** Completado en la rama `chore/update-readme-owasp`.
*   **Archivos Modificados:** `README.md`, `docs/AGENT_LOGS.md`.
*   **Hecho:** El usuario actualizó los prompts operativos en el `README.md` para incluir la validación obligatoria del nuevo documento `OWASP_TOP_10_2025_COMPLIANCE.md` tanto al iniciar como al finalizar futuras sesiones, garantizando así la permanencia de los controles de seguridad en todo el ciclo de vida de desarrollo.
*   **Siguiente paso:** Iniciar la Historia 1.5.10 (Control de Software Supply Chain Failures) en la próxima sesión.

---

### [2026-06-12] - Historia 1.5.10 y Actualización de Roadmap B2B (Antigravity / DevOps & Cloud Architect)
*   **Estado:** Completado en la rama `feature/1.5.10-supply-chain-failures`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `docs/BUSINESS_PRODUCT/DEFERRED_FEATURES.md`, `docs/SCRUM/KANBAN.md`, `docs/SCRUM/USER_STORY_MAP.md`, `docs/ENGINEERING_STANDARDS/DATA_ARCHITECTURE.md`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml`, `environment.yml`, `docs/AGENT_LOGS.md`.
*   **Hecho:** Se distribuyeron y ordenaron correctamente las propuestas arquitectónicas para los Sprints 4 al 8: Imputación KNN/MICE, Resiliencia Scraping, OLTP PostgreSQL, RLS para SaaS Multi-tenant, Cifrado at-rest/in-transit (ISO 27001), Data Lineage, Alta Disponibilidad e Integración CDC. Además, se documentó el diferimiento de Elasticsearch para la V4. Se completó la Historia 1.5.10 implementando `pip-audit` en el `environment.yml`, `pre-commit` y CI/CD para bloquear dependencias vulnerables en PRs (OWASP A03). Finalmente, se cerró formalmente el Sprint 1.
*   **Siguiente paso:** Iniciar el Sprint 2 con la Historia 2.1.1 (Análisis Exploratorio ydata-profiling).

---

### [2026-06-12] - Historia 2.1.1: Análisis Exploratorio con ydata-profiling (David / Data Analyst)
*   **Estado:** Completado en la rama `feature/2.1.1-ydata-profiling`.
*   **Vertical Slice:** 2 (Econometría Básica y Orquestación)
*   **Archivos Modificados:** `src/core/quality/silver_profiler.py`, `tests/test_silver_profiler.py`, `environment.yml`, `docs/SCRUM/KANBAN.md`, `docs/SCRUM/USER_STORY_MAP.md`, `docs/BUSINESS_PRODUCT/DEFERRED_FEATURES.md`, `docs/AGENT_LOGS.md`.
*   **Hecho:** Se implementó `SilverProfilerFacade` para generar perfiles HTML usando `ydata-profiling`. Se aplicó el principio SRP y un mecanismo de Degradación Elegante (Fallback) con Pandas en caso de fallo de memoria, protegiendo así el Lakehouse (ISO 22301 y MTPD). El reporte se mantuvo local para los analistas, aplazando la integración en Streamlit según se registró en `DEFERRED_FEATURES.md` (preservando ISO 25010 Interaction Capability). Se realizaron pruebas automatizadas que pasaron exitosamente y se documentó todo el seguimiento en el tablero Kanban.
*   **Siguiente paso:** Iniciar la Historia 2.2.1 (Modelo Logit Riesgo Churn).

---

### [2026-06-12] - Historia 2.1.2: Selección de Algoritmos Base con PyCaret (David / MLOps)
*   **Estado:** Completado en la rama `feature/2.1.2-pycaret-baseline-models`.
*   **Vertical Slice:** 2 (Econometría Básica y Orquestación)
*   **Archivos Modificados:** `environment.yml`, `src/core/interfaces/automl_interface.py`, `src/use_cases/automl_facade.py`, `tests/test_automl_facade.py`, `docs/SCRUM/KANBAN.md`, `docs/AGENT_LOGS.md`.
*   **Hecho:** Se implementó `AutoMLFacade` encapsulando `PyCaret` para generar y comparar modelos base. Se configuró el tracking de `MLflow` para registrar automáticamente métricas y matrices de confusión en local. Las dependencias se instalaron exitosamente utilizando `pip` para evitar fallos de conexión de Conda.
*   **Siguiente paso:** **Pivote estratégico (Acordado con el usuario):** Iniciar un nuevo chat de sesión para realizar una Extracción de Datos Reales (Scraping de App Store/Play Store reales) que sustituya la data *random* de prueba, asegurando la validez del análisis para la presentación final. Posterior a esto, se verá de reiniciar el sprint 2, ahora con los datos correctos.

---

### [2026-06-12] - Cierre de Sesión y Mantenimiento (Antigravity / Scrum Master)
*   **Estado:** Completado en la rama `chore/session-wrapup-sprint2`.
*   **Archivos Modificados:** `docs/SCRUM/KANBAN.md`, `docs/SCRUM/USER_STORY_MAP.md`, `docs/ADRs/ARCHITECTURE_DECISIONS.md`, `docs/BUSINESS_PRODUCT/DEFERRED_FEATURES.md`, `docs/AGENT_LOGS.md`.
*   **Hecho:** Se cerró formalmente la Historia 2.1.2 marcando los criterios de aceptación como completados. Se agregó el ADR 019 para asentar la decisión de mantener MLflow en local y se actualizó `DEFERRED_FEATURES.md` difiriendo Databricks MLflow al Release 3. Se verificó que todas las ISOs y principios SOLID se mantienen intactos.
*   **Siguiente paso:** Iniciar un nuevo chat para la Extracción de Datos Reales.

---

### [2026-06-13] - Sprint 1.5: Rehidratación de Datos Reales (Antigravity / Data Engineer)
*   **Estado:** Completado.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `src/core/config/app_targets.json`, `src/infrastructure/extractors/playstore_scraper.py`, `src/infrastructure/extractors/appstore_scraper.py`, `src/infrastructure/extractors/scraper_factory.py`, `src/orchestration/massive_extractor.py`.
*   **Hecho:** Se migró el pipeline para apuntar a IDs reales de las apps bancarias de Bolivia. Se resolvió un bucle infinito en la librería de Play Store cuando retornaba 0 reseñas. La extracción masiva de Android (Play Store) se completó exitosamente con 100% de tolerancia a fallos, implementando PII hashing (ISO 27001). Se comprobó que la librería `app_store_scraper` está actualmente inoperable por bloqueos en la API web de Apple (retorna HTML en vez de JSON), por lo que el scraper aplica degradación elegante retornando 0 reseñas para iOS sin romper el pipeline general.
*   **Siguiente paso:** Iniciar el re-procesamiento de las capas Silver y Gold en PySpark con los nuevos datos reales de la Play Store y continuar con el Sprint 2 (ML y Modelado).

---

### [2026-06-13] - Cierre Definitivo de Historia 1.5.11 y Limpieza App Store (Antigravity / Data Engineer)
*   **Estado:** Completado en la rama `feature/1.1.2-real-data-extraction`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `docs/APPSTORE_SCRAPING_STATUS.md` (creado), `docs/SCRUM/KANBAN.md`, `docs/SCRUM/USER_STORY_MAP.md`, `docs/BUSINESS_PRODUCT/DEFERRED_FEATURES.md`.
*   **Hecho:** Se desarrolló inicialmente una solución avanzada con Playwright para extraer las reseñas ocultas de la App Store que superó las restricciones (429 Too Many Requests), extrayendo usuarios anonimizados mediante SHA-256 de forma correcta. Sin embargo, para mantener el entorno ligero, estable y libre de dependencias complejas de scraping web headless (Playwright, Chromium), el usuario aprobó revertir todos los cambios, desinstalar Playwright, borrar los JSON generados de iOS en la capa Bronze y diferir oficialmente el scraping de iOS. Se documentó todo el análisis técnico en `APPSTORE_SCRAPING_STATUS.md` y se cerró completamente la Historia 1.5.11 marcándola finalizada en el Kanban.
*   **Siguiente paso:** Iniciar la Historia 1.5.12 (Refactorización a PySpark para Silver y Gold Layer).

---

### [2026-06-13] - Extracción Masiva Completa PlayStore (Antigravity / Data Engineer)
*   **Estado:** Completado en la rama `feature/full-playstore-extraction`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `src/orchestration/massive_extractor.py`, `docs/AGENT_LOGS.md`.
*   **Hecho:** Se eliminó el límite de prueba en `massive_extractor.py` (aumentando `max_reviews` a 1,000,000) y se ejecutó exitosamente la descarga masiva y completa de todas las reseñas reales disponibles en Google Play Store para los 8 bancos objetivos (BCP, Unión, BNB, BISA, BancoSol, Económico, Mercantil, Ganadero). Los datos se almacenaron anonimizados en la capa Bronze. Cumplimiento absoluto de ISO 27001 (PII), ITIL 4 (progreso iterativo) e ISO 22301 (backoff por Rate Limits).
*   **Siguiente paso:** Iniciar la Historia 1.5.12 (Refactorización a PySpark para Silver y Gold Layer) para procesar todo el nuevo volumen de datos masivos.

---

### [2026-06-13] - Historia 1.5.12: Refactorización a PySpark (Silver y Gold Layer) (Antigravity / Data Engineer)
*   **Estado:** Completado en la rama `feature/1.5.12-refactor-pyspark`.
*   **Vertical Slice:** 1 (Ingeniería de Datos Base e Infraestructura)
*   **Archivos Modificados:** `src/infrastructure/pipelines/silver_pipeline.py`, `src/infrastructure/pipelines/gold_pipeline.py`, `tests/test_silver_pipeline.py`, `tests/test_gold_pipeline.py`, `environment.yml`, `docs/SCRUM/KANBAN.md`, `docs/SCRUM/USER_STORY_MAP.md`.
*   **Hecho:** Se implementó `StructType` estricto en la capa Silver para validación robusta y optimización. Se desarrolló el mecanismo de Slowly Changing Dimensions (SCD Tipo 2) mediante `DeltaTable.merge()` en la capa Gold. Se refactorizaron y corrigieron los tests con una `SparkSession` local usando la extensión Delta. Finalmente se ajustó el archivo `environment.yml` anclando `pyspark=3.5.1` y `pandas=2.2.2` para resolver incompatibilidades de versiones con `delta-spark` en entornos de staging.
*   **Siguiente paso:** Iniciar el Sprint 2 con la Historia 2.2.1 (Modelo Logit Riesgo Churn).
