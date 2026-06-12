# Mapa de Historias de Usuario (Product Roadmap)

Este mapa define la visión del producto B2B SaaS a nivel Enterprise. La ejecución de las historias sigue la filosofía de **Vertical Slices**: no construimos capas aisladas, sino funcionalidades de extremo a extremo que aporten valor inmediato.

> **Leyenda de Puntos de Historia (Pts):**
> *   `3 Pts`: ~ 4 horas (Medio día)
> *   `5 Pts`: ~ 8 horas (1 día completo)
> *   `8 Pts`: ~ 12-16 horas (1.5 a 2 días)

---

# 🚀 RELEASE 1: MVP (Mínimo Producto Viable - Presentación Universitaria)

## 🟧 ACTIVIDAD 1: Data Engineering y DevOps (Cimientos y Lakehouse)

### 🟦 1.1 Scraping Básico (Vertical Slice 1)
**Historia 1.1.1: Factory de Scrapers y Extracción AppStore**
**Pts: 8** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito crear un patrón `Factory Method` para instanciar scrapers y extraer reseñas de las tiendas de apps de forma que podamos popular la capa Bronze.
*Criterios de Aceptación:*
[x] Clase `ScraperFactory` implementada.
[x] Código PySpark usando `google_play_scraper`.
[x] Idempotencia (no duplicar reseñas si se corre dos veces).
[x] Manejo de errores y paginación en las peticiones.

### 🟦 1.2 Seguridad, Gobernanza y Lakehouse (Rol: Cloud Architect)
**Historia 1.2.1: Singleton Database y Data Contracts**
**Pts: 8** | **Asignado a: David (Cloud Architect)**
Yo como Cloud Architect necesito configurar DuckDB/Databricks aplicando el patrón `Singleton` y contratos de datos estrictos (DIP) de forma que la basura de internet no contamine el análisis.
*Criterios de Aceptación:*
[x] Esquemas estrictos de tablas definidos con Pydantic.
[x] Conexión a DB implementada como Singleton para ahorrar memoria.
[x] Almacenamiento particionado en formato Parquet.

**Historia 1.2.2: Pipeline de Anonimización (ISO 27001)**
**Pts: 5** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito aplicar hashing SHA-256 a los nombres de usuarios e IPs de forma que cumplamos con las políticas de privacidad.
*Criterios de Aceptación:*
[x] Nombres de usuario totalmente irreconocibles en la capa Silver.

### 🟦 1.3 CI/CD y Automatización (Rol: DevOps Engineer)
**Historia 1.3.1: GitHub Actions y Pre-commits**
**Pts: 5** | **Asignado a: David (DevOps)**
Yo como DevOps Engineer necesito pipelines de CI/CD de forma que el código se pruebe automáticamente antes de un merge.
*Criterios de Aceptación:*
[x] Herramientas Ruff (Linter/Formatter) configuradas (ADR 012).
[x] GitHub Actions bloqueando pull requests que rompan el código.

### 🟦 1.4 Data Architecture y Transformación ELT (Rol: Data Engineer)
**Historia 1.4.0: Documentación de Arquitectura de Datos y Schemas**
**Pts: 3** | **Asignado a: David (Cloud Architect)**
Yo como Cloud Architect necesito documentar visualmente el viaje del dato (Medallón) y el diseño de la base de datos (Star Schema) de forma que los desarrolladores tengan un plano claro para construir la solución.
*Criterios de Aceptación:*
[x] Diagramas Mermaid Conceptual, Lógico y Físico creados.
[x] SCD Tipo 2 e integración del esquema de estrella justificados.

**Historia 1.4.1: Implementación Normativa ISO 27002 (Controles y Documentación)**
**Pts: 3** | **Asignado a: David (Cloud Architect)**
Yo como Cloud Architect necesito extraer y adecuar los lineamientos de la norma ISO/IEC 27002:2022 al contexto del proyecto SaaS de forma que cumplamos con los estándares de privacidad, seguridad y ciclo de vida de desarrollo seguro.
*Criterios de Aceptación:*
[x] Revisión del PDF y extracción de controles aplicables.
[x] Creación del documento base `ISO_27002_COMPLIANCE.md`.
[x] Actualización del mapa de usuario y políticas de DevOps/Seguridad.

**Historia 1.4.2: Pipeline de Transformación Silver y Calidad de Datos**
**Pts: 8** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito limpiar las reseñas y aplicar reglas de calidad (Data Observability) de forma que la capa Silver contenga datos confiables y tabulares listos para ML.
*Criterios de Aceptación:*
[x] Limpieza de nulos y duplicados implementada.
[x] Data Quality Checks (aserciones/expectativas) definidos.
[x] Cumplimiento de Data Masking (Control 8.11 ISO 27002) verificado.
[x] Archivos guardados particionados por año/mes.

**Historia 1.4.3: Construcción de Capa Gold (Star Schema y SCD Type 2)**
**Pts: 8** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito construir un Esquema de Estrella en la capa Gold implementando Dimensiones Lentamente Cambiantes (SCD Tipo 2) de forma que el Dashboard consulte rápido sin perder historial.
*Criterios de Aceptación:*
[x] Tabla Fact_Reviews creada con claves subrogadas.
[x] Dim_App creada con `valid_from`, `valid_to`, `is_current`.
[x] Modelo optimizado y persistido en DuckDB/Parquet.

### 🟦 1.5 Gobierno, Seguridad y Gestión de Servicios (ISO & ITIL 4) (Roles: Cloud Architect & DevOps)
**Historia 1.5.1: Documentación e Implementación del SVS de ITIL 4 y Principios Guía**
**Pts: 3** | **Asignado a: David (Cloud Architect)**
Yo como Cloud Architect necesito documentar la integración del Sistema de Valor del Servicio (SVS) de ITIL 4 y sus Principios Guía para que nuestra arquitectura técnica esté alineada con el valor de negocio.
*Criterios de Aceptación:*
[x] Archivo `ITIL_4_COMPLIANCE.md` creado.
[x] Principios Guía documentados en los manuales de trabajo (`HOW_WE_WORK.md`).
[x] ADR 015 generado.

**Historia 1.5.2: Auditoría ISMS y Prevención de Fugas de Datos (ISO 27001)**
**Pts: 5** | **Asignado a: David (Cloud Architect)**
Yo como Cloud Architect necesito implementar el tratamiento de riesgos, control de accesos lógico y logging centralizado de forma que se garantice la prevención de fuga de datos sensibles y el cumplimiento de ISO 27001 (Controles 8.12, 8.15, 6.1.2).
*Criterios de Aceptación:*
[x] Sistema de Logging centralizado configurado para el orquestador y scrapers.
[x] Evaluación de riesgos de extracción e ingesta documentada en los ADRs/Logs.
[x] Aislamiento de capas de datos (Bronze, Silver, Gold) protegido por diseño.

**Historia 1.5.3: Procesos de Mesa de Servicios y Gestión de Incidentes**
**Pts: 5** | **Asignado a: David (DevOps)**
Yo como DevOps Engineer necesito integrar una política clara de Mesa de Servicios e Incidentes de forma que podamos restaurar rápidamente cualquier caída de los scrapers o de la base de datos sin afectar el entorno de producción.
*Criterios de Aceptación:*
[x] Proceso de Mesa de Servicios definido.
[x] Política de respuesta a incidentes mayores (*swarming*) documentada y en uso.

**Historia 1.5.4: Gestión de Problemas y Habilitación del Cambio en CI/CD**
**Pts: 5** | **Asignado a: David (DevOps)**
Yo como DevOps Engineer necesito aplicar la Habilitación del Cambio (diferenciando Cambios Normales y Estándar) y documentar Errores Conocidos para minimizar la deuda técnica y riesgos.
*Criterios de Aceptación:*
[x] Pipeline de CI/CD ajustado como mecanismo de habilitación del cambio.
[x] Documentación para el seguimiento de Errores Conocidos y Soluciones Temporales (*Workarounds*) integrada en las políticas.

**Historia 1.5.5: Secure Development Life Cycle y Pruebas de Seguridad**
**Pts: 3** | **Asignado a: David (DevOps)**
Yo como DevOps Engineer necesito integrar controles de seguridad y escaneo en el ciclo de desarrollo de forma que las vulnerabilidades se detecten antes del paso a producción (ISO 27001 Controles 8.25, 8.28, 8.29).
*Criterios de Aceptación:*
[x] Integración de herramientas de escaneo de seguridad en GitHub Actions.
[x] Auditoría de secretos y credenciales en el código fuente.

**Historia 1.5.6: SGCN y Business Impact Analysis Básico (ISO 22301)**
**Pts: 5** | **Asignado a: David (Cloud Architect)**
Yo como Cloud Architect necesito definir el Sistema de Gestión de Continuidad de Negocio (SGCN) y el MTPD para establecer la resiliencia del pipeline de datos frente a incidentes.
*Criterios de Aceptación:*
[x] Elaboración de un Business Impact Analysis (BIA) inicial documentado.
[x] Identificación de los riesgos de interrupción más críticos y estrategias mitigantes base.

**Historia 1.5.7: Adecuación PIMS (ISO 27701) y Consentimiento de PII**
**Pts: 3** | **Asignado a: David (Cloud Architect)**
Yo como Cloud Architect necesito documentar e integrar el Sistema de Gestión de Información de Privacidad (PIMS) basado en ISO 27701, definiendo claramente nuestros roles como PII Processor/Controller de forma que cumplamos con los estándares de privacidad internacionales.
*Criterios de Aceptación:*
[x] Extracción y análisis de la ISO 27701 en `ISO_27701_COMPLIANCE.md`.
[x] Políticas de minimización y de-identificación validadas en arquitectura.

**Historia 1.5.8: Documentación del Modelo de Calidad ISO 25010 y DevSecOps**
**Pts: 3** | **Asignado a: David (Cloud Architect)**
Yo como Cloud Architect necesito destilar el estándar ISO 25010 y sus 9 características de calidad (incluyendo Safety e Interaction Capability) y alinearlas con nuestras prácticas DevOps.
*Criterios de Aceptación:*
[x] Análisis de los PDFs de contexto realizado.
[x] Archivo `ISO_25010_COMPLIANCE.md` creado.
[x] Puntos de calidad incorporados al Kanban y Roadmap.

**Historia 1.5.9: Integración Normativa OWASP Top 10 2025**
**Pts: 3** | **Asignado a: David (Cloud Architect)**
Yo como Cloud Architect necesito destilar el estándar OWASP Top 10 2025 para prevenir vulnerabilidades de software (A01-A10) en nuestra arquitectura.
*Criterios de Aceptación:*
[x] Archivo `OWASP_TOP_10_2025_COMPLIANCE.md` creado y validado.
[x] PDF original de OWASP procesado y eliminado para no saturar el repo.

**Historia 1.5.10: Control de Software Supply Chain Failures**
**Pts: 3** | **Asignado a: David (DevOps)**
Yo como DevOps Engineer necesito garantizar que nuestras dependencias y librerías no introduzcan vulnerabilidades o "Supply Chain Failures" (OWASP A03) mediante análisis de dependencias.
*Criterios de Aceptación:*
[x] Escáneres de dependencias añadidos en la validación local / CI.

## 🟧 ACTIVIDAD 2: Data Science, Econometría y MLOps

### 🟦 2.1 EDA y Auto-ML (Rol: Data Analyst)
**Historia 2.1.1: Análisis Exploratorio con ydata-profiling**
**Pts: 5** | **Asignado a: David (Data Analyst)**
Yo como Analista de Datos necesito generar reportes automáticos de calidad de forma que entienda la distribución estadística de la capa Silver.
*Criterios de Aceptación:*
[ ] Reporte HTML generado automáticamente en cada corrida.

**Historia 2.1.2: Selección de Algoritmos Base (PyCaret)**
**Pts: 8** | **Asignado a: David (MLOps)**
Yo como MLOps Engineer necesito usar PyCaret de forma que pueda entrenar y comparar rápidamente decenas de algoritmos antes del tuning fino.
*Criterios de Aceptación:*
[ ] Pipeline de PyCaret corriendo en MLflow.

### 🟦 2.2 Modelos Econométricos Core (Rol: Econometrista)
**Historia 2.2.1: Modelo Probit/Logit de Riesgo de Fuga (Churn)**
**Pts: 8** | **Asignado a: David (Econometrista)**
Yo como Econometrista necesito modelar la probabilidad de *Churn* usando `statsmodels` de forma que podamos alertar al banco sobre fallos críticos.
*Criterios de Aceptación:*
[ ] Variable Proxy de Churn creada y documentada.
[ ] Logit modelando la causalidad estadística.
[ ] Pruebas de heterocedasticidad superadas.

**Historia 2.2.2: Cálculo Econométrico del NPS**
**Pts: 5** | **Asignado a: David (Econometrista)**
Yo como Econometrista necesito calcular el Net Promoter Score en base a las estrellas.
*Criterios de Aceptación:*
[ ] Evolución temporal del NPS calculada (Promotores vs Detractores).

**Historia 2.2.3: Cadenas de Markov de Satisfacción**
**Pts: 8** | **Asignado a: David (Econometrista)**
Yo como Econometrista necesito modelar la matriz de transición de los usuarios (Satisfecho -> Frustrado -> Fuga) usando secuencias temporales.
*Criterios de Aceptación:*
[ ] Matriz de probabilidad de transición matemática validada.

### 🟦 2.3 Procesamiento de Lenguaje Natural (Rol: Data Scientist)
**Historia 2.3.1: Facade NLP y Clasificación de Sentimiento**
**Pts: 8** | **Asignado a: David (Data Scientist)**
Yo como Científico de Datos necesito aplicar el patrón `Facade` para ocultar la complejidad de HuggingFace y clasificar sentimientos.
*Criterios de Aceptación:*
[ ] Clase `NLPFacade` exponiendo un método simple `analyze()`.
[ ] Precisión > 85% en clasificación.

**Historia 2.3.2: Extracción Temática y Tracking (MLflow)**
**Pts: 5** | **Asignado a: David (MLOps)**
Yo como MLOps necesito trackear el modelo en MLflow.
*Criterios de Aceptación:*
[ ] Experimentos registrados sistemáticamente en MLflow local.

## 🟧 ACTIVIDAD 3: UI/UX y Orquestación

### 🟦 3.1 Orquestación y Patrón Command (Rol: Backend Developer)
**Historia 3.1.1: Menú Interactivo CLI (Capa 4)**
**Pts: 8** | **Asignado a: David (Desarrollador)**
Yo como Desarrollador necesito un menú CLI (`rich`) aplicando el patrón `Command` de forma que pueda orquestar todas las ejecuciones limpiamente.
*Criterios de Aceptación:*
[ ] Interfaz de consola con estilo visual.
[ ] Patrón Command encapsulando las órdenes del usuario.

### 🟦 3.2 Visualización Final y Observer (Rol: UI/UX Engineer)
**Historia 3.2.1: Streamlit Dashboard (Patrón F)**
**Pts: 8** | **Asignado a: David (UI/UX Engineer)**
Yo como UI/UX Engineer necesito diseñar la interfaz siguiendo la jerarquía visual del Patrón F, apoyándome en el patrón `Observer` para las métricas reactivas.
*Criterios de Aceptación:*
[ ] Gráficas Plotly avanzadas (sin espacios muertos).
[ ] KPIs claros en la parte superior (NPS, Churn Promedio).
[ ] Storytelling aplicado en la disposición visual.

**Historia 3.2.2: Pruebas de Interaction Capability y Usabilidad (ISO 25010)**
**Pts: 5** | **Asignado a: David (UI/UX Engineer)**
Yo como UI/UX Engineer necesito diseñar pruebas para validar la prevención de errores, operabilidad e inclusividad del Dashboard de acuerdo al estándar ISO 25010.
*Criterios de Aceptación:*
[ ] Validación de despliegue self-service implementado en Streamlit.
[ ] Diseño previene errores operacionales del usuario final.

---

# 🚀 RELEASE 2: B2B SaaS & Omnicanalidad (Comercialización)

### 🟦 4.1 Ingesta Omnicanal y Strategy (Rol: Data Engineer)
**Historia 4.1.1: Scraping Redes Multimedia usando Strategy (TikTok, IG)**
**Pts: 8** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito aplicar el patrón `Strategy` para alternar algoritmos de extracción entre APIs oficiales y scrapers web para redes multimedia.
*Criterios de Aceptación:*
[ ] Patrón Strategy funcional.
[ ] Integración a la capa Bronze.

**Historia 4.1.2: Scraping de Texto Corto (X, FB, Reddit, Trustpilot)**
**Pts: 8** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito un scraper para extraer texto puro de foros y Twitter.
*Criterios de Aceptación:*
[ ] Extracción con límites de Rate-Limit manejados.

**Historia 4.1.3: Manejo Avanzado de Valores Faltantes (MICE y KNN)**
**Pts: 5** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito aplicar técnicas avanzadas de imputación (MICE y KNN) en la capa Silver para variables secundarias, mejorando la completitud de la data sin distorsionar la distribución.
*Criterios de Aceptación:*
[ ] Imputación KNN y MICE implementadas y testeadas.

**Historia 4.1.4: Resiliencia de Scraping (Proxies) y Legalidad (TOS)**
**Pts: 5** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito configurar rotación de proxies y aplicar pausas aleatorias para evadir los bloqueos de Meta/Apple (TOS scraping bans), documentando nuestra justificación legal (ISO 27701).
*Criterios de Aceptación:*
[ ] Integración de un pool de proxies y backoff validado empíricamente.

### 🟦 4.2 Banking as a Service y Adapter (Rol: Backend Engineer)
**Historia 4.2.1: Arquitectura Base FastAPI usando Adapter**
**Pts: 8** | **Asignado a: David (Backend Engineer)**
Yo como Backend Engineer necesito levantar la API REST usando adaptadores (`Adapter Pattern`) para transformar el output de nuestros modelos al JSON esperado por los bancos.
*Criterios de Aceptación:*
[ ] Swagger interactivo.
[ ] Patrón Adapter implementado.

**Historia 4.2.2: Seguridad y Load Balancing API**
**Pts: 5** | **Asignado a: David (DevOps)**
Yo como DevOps necesito asegurar que la API no colapse bajo concurrencia.
*Criterios de Aceptación:*
[ ] Rate limiting implementado. Latencia < 200ms.

**Historia 4.2.3: Pruebas de Estrés y Rendimiento API (Performance Efficiency ISO 25010)**
**Pts: 5** | **Asignado a: David (DevOps)**
Yo como DevOps necesito validar el comportamiento de tiempo y utilización de recursos (DuckDB, PySpark) bajo estrés en la API, cumpliendo los criterios de "Performance Efficiency" de la ISO 25010.
*Criterios de Aceptación:*
[ ] Pruebas de carga usando Locust/K6 implementadas.
[ ] Auto-scaling (conceptos teóricos para Release 3) validado en staging.

**Historia 4.2.4: Prevención de Broken Access Control y SSRF**
**Pts: 5** | **Asignado a: David (Backend Engineer)**
Yo como Backend Engineer necesito implementar middlewares o decoradores en la API para asegurar que ningún endpoint de FastAPI sufra de Broken Access Control (OWASP A01) ni Server-Side Request Forgery (OWASP A10).
*Criterios de Aceptación:*
[ ] Endpoints bloqueados por defecto (Deny by default).
[ ] Control estricto de ownership en la lectura de datos de la API.

**Historia 4.2.5: Logging Activo y Alerting de Seguridad**
**Pts: 5** | **Asignado a: David (DevOps)**
Yo como DevOps necesito conectar el `AuditLogger` con notificaciones en tiempo real para anomalías de forma que podamos detectar y alertar ataques en tiempo real (OWASP A09).
*Criterios de Aceptación:*
[ ] Notificación proactiva si ocurre un error repetitivo de acceso no autorizado.

**Historia 4.2.6: Arquitectura OLTP vs OLAP y Row Level Security (RLS)**
**Pts: 8** | **Asignado a: David (Cloud Architect)**
Yo como Cloud Architect necesito levantar una base PostgreSQL transaccional (OLTP) para gestionar usuarios SaaS y facturación, separada del Lakehouse OLAP, e implementar Row Level Security (RLS) para que un cliente nunca vea datos de otro.
*Criterios de Aceptación:*
[ ] PostgreSQL OLTP en funcionamiento.
[ ] RLS testeado: User A no puede consultar `tenant_id` de User B.

**Historia 4.2.7: Audit Logs Administrativos (ISO 27001)**
**Pts: 3** | **Asignado a: David (DevOps)**
Yo como DevOps necesito que el `AuditLogger` registre invariablemente cualquier acción administrativa (creación de tenants, cambio de planes de facturación) para auditorías de seguridad.
*Criterios de Aceptación:*
[ ] Trazas de logs de acciones críticas persistidas y seguras.

### 🟦 4.3 Agentes B2B Conversacionales y Model Delivery (Rol: AI / DevOps)
**Historia 4.3.1: Setup Vector Database local (Chroma/FAISS)**
**Pts: 5** | **Asignado a: David (AI Engineer)**
Yo como AI Engineer necesito guardar las reseñas en embeddings.
*Criterios de Aceptación:*
[ ] Indexación correcta de documentos.

**Historia 4.3.2: Agente LangChain/LangGraph (Memoria)**
**Pts: 8** | **Asignado a: David (AI Engineer)**
Yo como AI Engineer necesito dotar de razonamiento iterativo (ReAct) al chatbot.
*Criterios de Aceptación:*
[ ] Memoria de sesión funcional mediante LangGraph.

**Historia 4.4.1: Canary Release y Blue-Green Deployment para Modelos**
**Pts: 8** | **Asignado a: David (DevOps)**
Yo como DevOps necesito diseñar una estrategia de despliegue progresivo (Canary) para los modelos NLP de manera que garanticemos fiabilidad y safety en entornos de producción.
*Criterios de Aceptación:*
[ ] Estrategia de enrutamiento parcial (10% tráfico a nuevo modelo) documentada e implementada en CI/CD.

---

# 🚀 RELEASE 3: Enterprise Scale (Visión a Largo Plazo)

### 🟦 5.1 Infraestructura Distribuida e IaC (Rol: Cloud Architect)
**Historia 5.1.1: Dockerización de Servicios**
**Pts: 5** | **Asignado a: David (DevOps)**
Yo como DevOps necesito meter todo el monolito en contenedores Docker.
*Criterios de Aceptación:*
[ ] Docker Compose funcionales sin errores de entorno.

**Historia 5.1.2: Infraestructura como Código (IaC) con Terraform**
**Pts: 8** | **Asignado a: David (Cloud Architect)**
Yo como Cloud Architect necesito provisionar los recursos de AWS/GCP (VPCs, S3) mediante código Terraform para garantizar portabilidad y evitar "configuration drift".
*Criterios de Aceptación:*
[ ] Módulos Terraform de red, storage y compute generados y funcionales.

**Historia 5.1.3: Migración a Kubernetes (K8s) (EKS/GKE)**
**Pts: 8** | **Asignado a: David (Cloud Architect)**
Yo como Cloud Architect necesito levantar un cluster Kubernetes para orquestar los contenedores y manejar la resiliencia en alto estrés.
*Criterios de Aceptación:*
[ ] Cluster y Auto-scaling (HPA) configurados.

**Historia 5.1.4: Implementación de Rolling Updates en K8s**
**Pts: 5** | **Asignado a: David (DevOps)**
Yo como DevOps necesito configurar Rolling Updates en K8s de modo que las actualizaciones a contenedores ocurran sin pérdida de disponibilidad.
*Criterios de Aceptación:*
[ ] Configuración de Rolling Update y `readinessProbe` lista en los manifiestos de Deployment.

**Historia 5.1.5: Cifrado en Tránsito y Reposo (ISO 27001)**
**Pts: 5** | **Asignado a: David (Cloud Architect)**
Yo como Cloud Architect necesito configurar cifrado KMS (AES-256) en los buckets S3 de la capa Bronze y forzar TLS en todas las comunicaciones del pipeline para cumplir estrictamente con los controles de ISO 27001.
*Criterios de Aceptación:*
[ ] Todos los datos at rest están cifrados automáticamente.
[ ] Endpoints de ingesta rechazan peticiones sin HTTPS.

### 🟦 5.2 Streaming en Tiempo Real (Rol: Data Engineer)
**Historia 5.2.1: Setup Apache Kafka Cluster**
**Pts: 5** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito un broker Kafka para los flujos.
*Criterios de Aceptación:*
[ ] Kafka levantado.

**Historia 5.2.2: Producers y Consumers**
**Pts: 8** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito ingestar reseñas en Tiempo Real sub-segundo.

**Historia 5.2.3: Carga Incremental (CDC) y Data Lineage**
**Pts: 8** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito implementar Change Data Capture (CDC) para inyectar solo registros nuevos en lugar de procesar por lotes completos, y documentar visualmente el Data Lineage / DAG completo.
*Criterios de Aceptación:*
[ ] CDC funcional reduciendo el overhead de I/O en la capa Bronze a Silver.
[ ] Diagrama de linaje generado en la documentación.

### 🟦 5.3 Continuidad y Disaster Recovery (Rol: Cloud Architect / DevOps)
**Historia 5.3.1: Automatización de Backups y Snapshots Cíclicos**
**Pts: 5** | **Asignado a: David (Cloud Architect)**
Yo como Cloud Architect necesito implementar respaldos automatizados de la capa Bronze y bases de datos para garantizar la integridad frente a corrupciones accidentales.
*Criterios de Aceptación:*
[ ] Scripts de backup a almacenamiento secundario (S3/GCS).
[ ] Verificación de integridad de los respaldos automatizada.

**Historia 5.3.2: Simulacros de Recuperación y Resiliencia (Disaster Recovery)**
**Pts: 8** | **Asignado a: David (DevOps)**
Yo como DevOps necesito programar simulacros de desastres donde las capas superiores son borradas para comprobar si los mecanismos de recuperación restauran la analítica en el MTPD esperado.
*Criterios de Aceptación:*
[ ] Prueba documentada de borrado de capa Silver y Gold, y regeneración.
[ ] Tiempo de regeneración dentro de los SLAs esperados.

**Historia 5.3.3: Ingeniería de Caos y Pruebas de Safety (ISO 25010)**
**Pts: 5** | **Asignado a: David (DevOps)**
Yo como DevOps necesito aplicar principios de Chaos Engineering (apagar instancias aleatoriamente) para validar la característica "Safety" (Mecanismos Fail Safe) del ISO 25010.
*Criterios de Aceptación:*
[ ] Entorno sobrevive a la pérdida aleatoria del servicio de NLP (Degradación Elegante).

**Historia 5.3.4: Alta Disponibilidad y Réplicas (ISO 22301)**
**Pts: 5** | **Asignado a: David (Cloud Architect)**
Yo como Cloud Architect necesito configurar réplicas de lectura transaccionales para la base de datos OLTP de forma que soportemos interrupciones en la zona principal y se respete el RTO.
*Criterios de Aceptación:*
[ ] Failover probado exitosamente (apagar nodo master y nodo esclavo asume control).

---

# 🚀 RELEASE 4: Enterprise Deep Listening & Multimodal AI (Visión Comercial)

### 🟦 6.1 Open Source Intelligence (OSINT) & Deep Web Crawling (Rol: Data Engineer)
**Historia 6.1.1: Web Crawler de Menciones de Marca (News & Blogs)**
**Pts: 8** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito implementar un scraper asíncrono para navegar la web abierta y foros buscando menciones directas.
*Criterios de Aceptación:*
[ ] Búsquedas heurísticas fuera de redes estructuradas implementadas.

**Historia 6.1.2: Integración de APIs de Búsqueda Profunda (SERP)**
**Pts: 5** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito integrarme a APIs de motores de búsqueda para extraer quejas en páginas de terceros (ej. foros de quejas).
*Criterios de Aceptación:*
[ ] API de SERP implementada y conectada al orquestador.

### 🟦 6.2 Inteligencia Artificial Multimodal (Rol: AI Engineer)
**Historia 6.2.1: Pipeline de Transcripción de Video/Audio (OpenAI Whisper)**
**Pts: 8** | **Asignado a: David (AI Engineer)**
Yo como AI Engineer necesito descargar audios de reseñas en video (YouTube/TikTok) y usar un modelo como Whisper para transcribir la voz a texto.
*Criterios de Aceptación:*
[ ] Pipeline de audio a texto funcional e integrado a la capa de NLP existente.

**Historia 6.2.2: OCR y Análisis de Imágenes (Vision Models)**
**Pts: 8** | **Asignado a: David (AI Engineer)**
Yo como AI Engineer necesito usar un modelo de visión computacional para extraer texto de capturas de pantalla compartidas por clientes enojados.
*Criterios de Aceptación:*
[ ] Extracción OCR exitosa en imágenes compartidas.
