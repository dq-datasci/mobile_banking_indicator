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
**Pts: 8** | **Asignado a: Boris (Cloud Architect)**
Yo como Cloud Architect necesito configurar DuckDB/Databricks aplicando el patrón `Singleton` y contratos de datos estrictos (DIP) de forma que la basura de internet no contamine el análisis.
*Criterios de Aceptación:*
[x] Esquemas estrictos de tablas definidos con Pydantic.
[x] Conexión a DB implementada como Singleton para ahorrar memoria.
[x] Almacenamiento particionado en formato Parquet.

**Historia 1.2.2: Pipeline de Anonimización (ISO 27001)**
**Pts: 5** | **Asignado a: Boris (Data Engineer)**
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
**Pts: 3** | **Asignado a: Boris (Cloud Architect)**
Yo como Cloud Architect necesito documentar visualmente el viaje del dato (Medallón) y el diseño de la base de datos (Star Schema) de forma que los desarrolladores tengan un plano claro para construir la solución.
*Criterios de Aceptación:*
[x] Diagramas Mermaid Conceptual, Lógico y Físico creados.
[x] SCD Tipo 2 e integración del esquema de estrella justificados.

**Historia 1.4.1: Implementación Normativa ISO 27002 (Controles y Documentación)**
**Pts: 3** | **Asignado a: Boris (Cloud Architect)**
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
[ ] Tabla Fact_Reviews creada con claves subrogadas.
[ ] Dim_App creada con `valid_from`, `valid_to`, `is_current`.
[ ] Modelo optimizado y persistido en DuckDB/Parquet.

## 🟧 ACTIVIDAD 2: Data Science, Econometría y MLOps

### 🟦 2.1 EDA y Auto-ML (Rol: Data Analyst)
**Historia 2.1.1: Análisis Exploratorio con ydata-profiling**
**Pts: 5** | **Asignado a: Boris (Data Analyst)**
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
**Pts: 8** | **Asignado a: Boris (Econometrista)**
Yo como Econometrista necesito modelar la probabilidad de *Churn* usando `statsmodels` de forma que podamos alertar al banco sobre fallos críticos.
*Criterios de Aceptación:*
[ ] Variable Proxy de Churn creada y documentada.
[ ] Logit modelando la causalidad estadística.
[ ] Pruebas de heterocedasticidad superadas.

**Historia 2.2.2: Cálculo Econométrico del NPS**
**Pts: 5** | **Asignado a: Boris (Econometrista)**
Yo como Econometrista necesito calcular el Net Promoter Score en base a las estrellas.
*Criterios de Aceptación:*
[ ] Evolución temporal del NPS calculada (Promotores vs Detractores).

**Historia 2.2.3: Cadenas de Markov de Satisfacción**
**Pts: 8** | **Asignado a: Boris (Econometrista)**
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
**Pts: 8** | **Asignado a: Boris (UI/UX Engineer)**
Yo como UI/UX Engineer necesito diseñar la interfaz siguiendo la jerarquía visual del Patrón F, apoyándome en el patrón `Observer` para las métricas reactivas.
*Criterios de Aceptación:*
[ ] Gráficas Plotly avanzadas (sin espacios muertos).
[ ] KPIs claros en la parte superior (NPS, Churn Promedio).
[ ] Storytelling aplicado en la disposición visual.

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

### 🟦 4.3 Agentes B2B Conversacionales (Rol: AI Engineer)
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

---

# 🚀 RELEASE 3: Enterprise Scale (Visión a Largo Plazo)

### 🟦 5.1 Infraestructura Distribuida (Rol: Cloud Architect)
**Historia 5.1.1: Dockerización de Servicios**
**Pts: 5** | **Asignado a: Boris (DevOps)**
Yo como DevOps necesito meter todo el monolito en contenedores Docker.
*Criterios de Aceptación:*
[ ] Docker Compose funcionales sin errores de entorno.

**Historia 5.1.2: Migración a Kubernetes (K8s)**
**Pts: 8** | **Asignado a: Boris (Cloud Architect)**
Yo como Cloud Architect necesito levantar un cluster EKS para orquestar los contenedores.
*Criterios de Aceptación:*
[ ] Auto-scaling (HPA) configurado.

### 🟦 5.2 Streaming en Tiempo Real (Rol: Data Engineer)
**Historia 5.2.1: Setup Apache Kafka Cluster**
**Pts: 5** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito un broker Kafka para los flujos.
*Criterios de Aceptación:*
[ ] Kafka levantado.

**Historia 5.2.2: Producers y Consumers**
**Pts: 8** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito ingestar reseñas en Tiempo Real sub-segundo.

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
