# Mapa de Historias de Usuario (Product Roadmap)

Este mapa define la visión del producto B2B SaaS a nivel Enterprise. Las historias están segregadas por el Rol Profesional requerido para su ejecución.

---

## 🟧 ACTIVIDAD 1: Data Engineering y DevOps (Cimientos y Lakehouse)

### 🟦 1.1 Scraping Omnicanal (Rol: Data Engineer)
**Historia 1.1.1: Ingresas de Datos - PlayStore y AppStore**
Yo como Data Engineer necesito un scraper en PySpark que extraiga reseñas de las tiendas de apps de forma que podamos popular la capa Bronze.

**Historia 1.1.2: Ingesta de Redes Sociales (TikTok, IG, FB, X, Reddit)**
Yo como Data Engineer necesito scrapers usando el Patrón Strategy (ej. Apify/Selenium) de forma que captemos la Voz del Cliente omnicanal.

### 🟦 1.2 Seguridad, Gobernanza y Lakehouse (Rol: Data Engineer / Cloud Architect)
**Historia 1.2.1: Lakehouse y Data Contracts**
Yo como Cloud Architect necesito configurar DuckDB/Databricks con contratos de datos estrictos de forma que la basura de internet no contamine el análisis.

**Historia 1.2.2: Pipeline de Anonimización (ISO 27001)**
Yo como Data Engineer necesito aplicar hashing SHA-256 a los nombres de usuarios de forma que cumplamos con las políticas de privacidad.

### 🟦 1.3 CI/CD y Automatización (Rol: DevOps Engineer)
**Historia 1.3.1: GitHub Actions y Pre-commits**
Yo como DevOps Engineer necesito pipelines de CI/CD de forma que el código se pruebe automáticamente antes de un merge.

---

## 🟧 ACTIVIDAD 2: Data Science, Econometría y MLOps

### 🟦 2.1 EDA y Auto-ML (Rol: Data Analyst / MLOps Engineer)
**Historia 2.1.1: Análisis Exploratorio con ydata-profiling**
Yo como Analista de Datos necesito generar reportes automáticos de calidad de forma que entienda la distribución estadística de la capa Silver.

**Historia 2.1.2: Selección de Algoritmos Base (PyCaret)**
Yo como MLOps Engineer necesito usar PyCaret de forma que pueda entrenar y comparar rápidamente decenas de algoritmos antes del tuning fino.

### 🟦 2.2 Modelos Econométricos Avanzados (Rol: Econometrista)
**Historia 2.2.1: Modelo Probit/Logit de Riesgo de Fuga**
Yo como Econometrista necesito modelar la probabilidad de *Churn* de forma que podamos alertar al banco sobre fallos críticos.

**Historia 2.2.2: Cadenas de Markov de Satisfacción**
Yo como Econometrista necesito modelar la matriz de transición de los usuarios (Satisfecho -> Frustrado -> Fuga).

### 🟦 2.3 Procesamiento de Lenguaje Natural (Rol: Data Scientist)
**Historia 2.3.1: Clasificador de Sentimiento con LangChain**
Yo como Científico de Datos necesito integrar agentes NLP robustos de forma que extraiga intenciones y sentimientos de los textos omnicanal.

---

## 🟧 ACTIVIDAD 3: UI/UX y Plataforma B2B (Banking as a Service)

### 🟦 3.1 Agentes Conversacionales (Rol: AI Engineer)
**Historia 3.1.1: Agente LangGraph (RAG)**
Yo como AI Engineer necesito un asistente conversacional con memoria (LangGraph) de forma que el ejecutivo bancario pueda chatear con los datos.

### 🟦 3.2 Backend y APIs (Rol: Backend Engineer)
**Historia 3.2.1: FastAPI B2B Endpoint**
Yo como Backend Engineer necesito exponer los modelos en una API REST de forma que otros bancos puedan comprar el acceso a nuestra tecnología.

### 🟦 3.3 Dashboard Interactivo (Rol: UI/UX Engineer)
**Historia 3.3.1: Streamlit Dashboard (Patrón F)**
Yo como UI/UX Engineer necesito diseñar la interfaz siguiendo la jerarquía visual del Patrón F y *Storytelling* de forma que los gerentes tomen decisiones en segundos.
