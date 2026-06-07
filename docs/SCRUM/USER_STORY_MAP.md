# Mapa de Historias de Usuario (Product Roadmap)

Este mapa define la visión del producto B2B SaaS a nivel Enterprise. Las historias están segregadas por el Rol Profesional requerido para su ejecución.

---

## 🟧 ACTIVIDAD 1: Data Engineering y DevOps (Cimientos y Lakehouse)

### 🟦 1.1 Scraping Omnicanal (Rol: Data Engineer)
**Historia 1.1.1: Ingesta de Datos - PlayStore y AppStore**
**Pts: 8** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito un scraper en PySpark que extraiga reseñas de las tiendas de apps de forma que podamos popular la capa Bronze.
*Criterios de Aceptación:*
[ ] Código PySpark usando `google_play_scraper`.
[ ] Idempotencia (no duplicar reseñas si se corre dos veces).

**Historia 1.1.2: Ingesta de Redes Sociales (TikTok, IG, FB, X, Trustpilot, Reddit)**
**Pts: 13** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito scrapers usando el Patrón Strategy (ej. Apify/Selenium) de forma que captemos la Voz del Cliente omnicanal.
*Criterios de Aceptación:*
[ ] Esqueleto del Patrón Strategy implementado.
[ ] Extracción funcional para al menos una red (para el MVP).

### 🟦 1.2 Seguridad, Gobernanza y Lakehouse (Rol: Data Engineer / Cloud Architect)
**Historia 1.2.1: Lakehouse y Data Contracts**
**Pts: 8** | **Asignado a: Boris (Cloud Architect)**
Yo como Cloud Architect necesito configurar DuckDB/Databricks con contratos de datos estrictos de forma que la basura de internet no contamine el análisis.
*Criterios de Aceptación:*
[ ] Esquemas estrictos de tablas.
[ ] Almacenamiento particionado en Parquet.

**Historia 1.2.2: Pipeline de Anonimización (ISO 27001)**
**Pts: 5** | **Asignado a: Boris (Data Engineer)**
Yo como Data Engineer necesito aplicar hashing SHA-256 a los nombres de usuarios e IPs de forma que cumplamos con las políticas de privacidad.
*Criterios de Aceptación:*
[ ] Nombres de usuario irreconocibles en la capa Silver.

### 🟦 1.3 CI/CD y Automatización (Rol: DevOps Engineer)
**Historia 1.3.1: GitHub Actions y Pre-commits**
**Pts: 5** | **Asignado a: David (DevOps)**
Yo como DevOps Engineer necesito pipelines de CI/CD de forma que el código se pruebe automáticamente antes de un merge.
*Criterios de Aceptación:*
[ ] Flake8 y Black configurados.
[ ] Actions bloqueando merges rotos.

---

## 🟧 ACTIVIDAD 2: Data Science, Econometría y MLOps

### 🟦 2.1 EDA y Auto-ML (Rol: Data Analyst / MLOps Engineer)
**Historia 2.1.1: Análisis Exploratorio con ydata-profiling**
**Pts: 5** | **Asignado a: Boris (Data Analyst)**
Yo como Analista de Datos necesito generar reportes automáticos de calidad de forma que entienda la distribución estadística de la capa Silver.
*Criterios de Aceptación:*
[ ] Reporte HTML generado automáticamente.

**Historia 2.1.2: Selección de Algoritmos Base (PyCaret)**
**Pts: 8** | **Asignado a: David (MLOps)**
Yo como MLOps Engineer necesito usar PyCaret de forma que pueda entrenar y comparar rápidamente decenas de algoritmos antes del tuning fino.
*Criterios de Aceptación:*
[ ] Pipeline de PyCaret corriendo en MLflow.

### 🟦 2.2 Modelos Econométricos Avanzados (Rol: Econometrista)
**Historia 2.2.1: Modelo Probit/Logit de Riesgo de Fuga y NPS**
**Pts: 13** | **Asignado a: Boris (Econometrista)**
Yo como Econometrista necesito modelar la probabilidad de *Churn* y calcular el NPS (Net Promoter Score) de forma que podamos alertar al banco sobre fallos críticos y la lealtad del cliente.
*Criterios de Aceptación:*
[ ] Variable Proxy de Churn creada en base al sentimiento y puntaje.
[ ] NPS calculado (Promotores vs Detractores).
[ ] Logit modelando la causalidad estadística.

**Historia 2.2.2: Cadenas de Markov de Satisfacción**
**Pts: 8** | **Asignado a: Boris (Econometrista)**
Yo como Econometrista necesito modelar la matriz de transición de los usuarios (Satisfecho -> Frustrado -> Fuga) usando secuencias temporales.
*Criterios de Aceptación:*
[ ] Matriz de transición calculada.

### 🟦 2.3 Procesamiento de Lenguaje Natural (Rol: Data Scientist)
**Historia 2.3.1: Clasificador NLP Omnicanal**
**Pts: 13** | **Asignado a: David (Data Scientist)**
Yo como Científico de Datos necesito un modelo NLP de forma que extraiga sentimientos e intenciones (Problema de Login, Fraude, Interfaz) de los textos omnicanal.
*Criterios de Aceptación:*
[ ] Modelo guardado y versionado.
[ ] Precisión > 85%.

---

## 🟧 ACTIVIDAD 3: UI/UX, Orquestación y Plataforma B2B

### 🟦 3.1 Orquestación y CLI Interactiva (Rol: Backend Developer)
**Historia 3.1.1: Menú Interactivo (Capa 4 - Orchestrator)**
**Pts: 8** | **Asignado a: David (Desarrollador)**
Yo como Desarrollador necesito un menú CLI interactivo (usando la librería `rich`) de forma que pueda orquestar todas las ejecuciones de los pipelines.
*Criterios de Aceptación:*
[ ] Interfaz de consola hermosa y profesional.
[ ] Manejo robusto de errores sin crashear.

### 🟦 3.2 Agentes Conversacionales (Rol: AI Engineer)
**Historia 3.2.1: Agente LangChain/LangGraph (RAG)**
**Pts: 13** | **Asignado a: David (AI Engineer)**
Yo como AI Engineer necesito un asistente conversacional con estado (LangGraph) de forma que el ejecutivo bancario pueda consultar con lenguaje natural las quejas de sus clientes.
*Criterios de Aceptación:*
[ ] RAG conectado a la base de datos de reseñas.

### 🟦 3.3 Backend y APIs (Rol: Backend Engineer)
**Historia 3.3.1: FastAPI B2B Endpoint**
**Pts: 13** | **Asignado a: David (Backend Engineer)**
Yo como Backend Engineer necesito exponer los modelos en una API REST de forma que otros bancos puedan comprar el acceso a nuestra tecnología BaaS.
*Criterios de Aceptación:*
[ ] Endpoint Swagger funcional.

### 🟦 3.4 Visualización Final (Rol: UI/UX Engineer)
**Historia 3.4.1: Streamlit Dashboard (Patrón F y KPIs)**
**Pts: 8** | **Asignado a: Boris (UI/UX Engineer)**
Yo como UI/UX Engineer necesito diseñar el Dashboard siguiendo la jerarquía visual del Patrón F de forma que se muestre el NPS, Market Share y la evolución del riesgo de fuga.
*Criterios de Aceptación:*
[ ] Gráficas Plotly avanzadas.
[ ] Storytelling aplicado (Qué, Por qué, Qué hacer).
