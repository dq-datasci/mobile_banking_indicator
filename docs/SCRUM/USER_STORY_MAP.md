# Mapa de Historias de Usuario (Product Roadmap)

Este mapa define la visión del producto B2B SaaS a nivel Enterprise. Las historias están segregadas por el Rol Profesional.

> **Leyenda de Puntos de Historia (Pts):** 
> *   `3 Pts`: ~ 4 horas (Medio día)
> *   `5 Pts`: ~ 8 horas (1 día completo)
> *   `8 Pts`: ~ 12-16 horas (1.5 a 2 días)
> *NOTA: Las tareas de más de 8 Pts se han subdividido para garantizar entregas ágiles.*

---

# 🚀 RELEASE 1: MVP (Mínimo Producto Viable - Presentación Universitaria)
*Objetivo:* Demostrar el valor econométrico y de IA usando datos reales de tiendas de aplicaciones.

## 🟧 ACTIVIDAD 1: Data Engineering y DevOps (Cimientos y Lakehouse)

### 🟦 1.1 Scraping Básico (Rol: Data Engineer)
**Historia 1.1.1: Ingesta de Datos - PlayStore y AppStore**
**Pts: 8** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito un scraper en PySpark que extraiga reseñas de las tiendas de apps de forma que podamos popular la capa Bronze.
*Criterios de Aceptación:*
[ ] Código PySpark usando `google_play_scraper`.
[ ] Idempotencia (no duplicar reseñas si se corre dos veces).
[ ] Manejo de errores y paginación en las peticiones.

### 🟦 1.2 Seguridad, Gobernanza y Lakehouse (Rol: Data Engineer / Cloud Architect)
**Historia 1.2.1: Lakehouse y Data Contracts**
**Pts: 8** | **Asignado a: Boris (Cloud Architect)**
Yo como Cloud Architect necesito configurar DuckDB/Databricks con contratos de datos estrictos de forma que la basura de internet no contamine el análisis.
*Criterios de Aceptación:*
[ ] Esquemas estrictos de tablas definidos con Pydantic/PySpark.
[ ] Almacenamiento particionado en formato Parquet.
[ ] Validación de nulos y tipos de datos en la ingesta.

**Historia 1.2.2: Pipeline de Anonimización (ISO 27001)**
**Pts: 5** | **Asignado a: Boris (Data Engineer)**
Yo como Data Engineer necesito aplicar hashing SHA-256 a los nombres de usuarios e IPs de forma que cumplamos con las políticas de privacidad.
*Criterios de Aceptación:*
[ ] Nombres de usuario totalmente irreconocibles en la capa Silver.
[ ] Semilla criptográfica guardada de forma segura.

### 🟦 1.3 CI/CD y Automatización (Rol: DevOps Engineer)
**Historia 1.3.1: GitHub Actions y Pre-commits**
**Pts: 5** | **Asignado a: David (DevOps)**
Yo como DevOps Engineer necesito pipelines de CI/CD de forma que el código se pruebe automáticamente antes de un merge.
*Criterios de Aceptación:*
[ ] Herramientas Flake8 y Black configuradas.
[ ] GitHub Actions bloqueando pull requests que rompan el código.

## 🟧 ACTIVIDAD 2: Data Science, Econometría y MLOps

### 🟦 2.1 EDA y Auto-ML (Rol: Data Analyst / MLOps Engineer)
**Historia 2.1.1: Análisis Exploratorio con ydata-profiling**
**Pts: 5** | **Asignado a: Boris (Data Analyst)**
Yo como Analista de Datos necesito generar reportes automáticos de calidad de forma que entienda la distribución estadística de la capa Silver.
*Criterios de Aceptación:*
[ ] Reporte HTML generado automáticamente en cada corrida.
[ ] Identificación de valores atípicos (outliers).

**Historia 2.1.2: Selección de Algoritmos Base (PyCaret)**
**Pts: 8** | **Asignado a: David (MLOps)**
Yo como MLOps Engineer necesito usar PyCaret de forma que pueda entrenar y comparar rápidamente decenas de algoritmos antes del tuning fino.
*Criterios de Aceptación:*
[ ] Pipeline de PyCaret integrado.
[ ] Resultados base exportados para revisión.

### 🟦 2.2 Modelos Econométricos Core (Rol: Econometrista)
**Historia 2.2.1: Modelo Probit/Logit de Riesgo de Fuga (Churn)**
**Pts: 8** | **Asignado a: Boris (Econometrista)**
Yo como Econometrista necesito modelar la probabilidad de *Churn* de forma que podamos alertar al banco sobre fallos críticos.
*Criterios de Aceptación:*
[ ] Variable Proxy de Churn creada y documentada.
[ ] Logit modelando la causalidad estadística con `statsmodels`.
[ ] Pruebas de heterocedasticidad superadas.

**Historia 2.2.2: Cálculo Econométrico del NPS**
**Pts: 5** | **Asignado a: Boris (Econometrista)**
Yo como Econometrista necesito calcular el Net Promoter Score en base a las estrellas.
*Criterios de Aceptación:*
[ ] Segmentación correcta de Promotores (4-5), Pasivos (3), Detractores (1-2).
[ ] Evolución temporal del NPS calculada.

**Historia 2.2.3: Cadenas de Markov de Satisfacción**
**Pts: 8** | **Asignado a: Boris (Econometrista)**
Yo como Econometrista necesito modelar la matriz de transición de los usuarios (Satisfecho -> Frustrado -> Fuga) usando secuencias temporales.
*Criterios de Aceptación:*
[ ] Estados discretos definidos.
[ ] Matriz de probabilidad de transición matemática validada.

### 🟦 2.3 Procesamiento de Lenguaje Natural (Rol: Data Scientist)
**Historia 2.3.1: Clasificador NLP (Modelo Base HuggingFace)**
**Pts: 8** | **Asignado a: David (Data Scientist)**
Yo como Científico de Datos necesito un modelo NLP de forma que extraiga sentimientos de las reseñas.
*Criterios de Aceptación:*
[ ] Modelo NLP cargado e infiriendo sobre el texto limpio.
[ ] Precisión > 85% en clasificación Positivo/Negativo/Neutro.

**Historia 2.3.2: Extracción de Entidades y Tracking (MLflow)**
**Pts: 5** | **Asignado a: David (MLOps / Data Scientist)**
Yo como Científico de Datos necesito extraer temáticas (Login, Fraude) y trackear el modelo en MLflow.
*Criterios de Aceptación:*
[ ] Extracción de la temática principal (Topic Modeling / NER).
[ ] Experimentos registrados sistemáticamente en MLflow local.

## 🟧 ACTIVIDAD 3: UI/UX y Orquestación

### 🟦 3.1 Orquestación (Rol: Backend Developer)
**Historia 3.1.1: Menú Interactivo (Capa 4 - Orchestrator)**
**Pts: 8** | **Asignado a: David (Desarrollador)**
Yo como Desarrollador necesito un menú CLI interactivo (usando la librería `rich`) de forma que pueda orquestar todas las ejecuciones.
*Criterios de Aceptación:*
[ ] Interfaz de consola con estilo visual (Grid/Panels).
[ ] Manejo robusto de excepciones.
[ ] Idempotencia en la ejecución.

### 🟦 3.2 Visualización Final (Rol: UI/UX Engineer)
**Historia 3.2.1: Streamlit Dashboard (Patrón F)**
**Pts: 8** | **Asignado a: Boris (UI/UX Engineer)**
Yo como UI/UX Engineer necesito diseñar la interfaz siguiendo la jerarquía visual del Patrón F.
*Criterios de Aceptación:*
[ ] Gráficas Plotly avanzadas (sin espacios muertos).
[ ] KPIs claros en la parte superior (NPS, Churn Promedio).
[ ] Storytelling aplicado en la disposición visual.

---

# 🚀 RELEASE 2: B2B SaaS & Omnicanalidad (Comercialización)
*Objetivo:* Expandir la ingesta a todas las redes y crear la API para vender el servicio.

### 🟦 4.1 Ingesta Omnicanal (Rol: Data Engineer)
**Historia 4.1.1: Scraping Redes de Videos y Fotos (TikTok, IG)**
**Pts: 8** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito un scraper para extraer quejas de TikTok e Instagram.
*Criterios de Aceptación:*
[ ] Scraper configurado superando bloqueos básicos.
[ ] Integración a la capa Bronze.

**Historia 4.1.2: Scraping de Texto Corto y Foros (X, FB, Reddit, Trustpilot)**
**Pts: 8** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito un scraper para extraer texto puro de foros y Twitter.
*Criterios de Aceptación:*
[ ] Extracción con límites de Rate-Limit manejados.
[ ] Limpieza de hashtags y arrobas en capa Silver.

### 🟦 4.2 Banking as a Service (Rol: Backend Engineer)
**Historia 4.2.1: Arquitectura Base FastAPI y Swagger**
**Pts: 8** | **Asignado a: David (Backend Engineer)**
Yo como Backend Engineer necesito levantar la API REST.
*Criterios de Aceptación:*
[ ] Swagger interactivo con documentación clara.
[ ] Endpoint funcional que recibe un texto y devuelve el riesgo de churn.

**Historia 4.2.2: Seguridad y Load Balancing API**
**Pts: 5** | **Asignado a: David (DevOps)**
Yo como DevOps necesito asegurar que la API no colapse bajo concurrencia.
*Criterios de Aceptación:*
[ ] Rate limiting implementado en el backend.
[ ] Tiempos de respuesta (Latencia) < 200ms.

### 🟦 4.3 Agentes B2B Conversacionales (Rol: AI Engineer)
**Historia 4.3.1: Setup Vector Database local (Chroma/FAISS)**
**Pts: 5** | **Asignado a: David (AI Engineer)**
Yo como AI Engineer necesito guardar las reseñas en embeddings vectoriales para búsqueda semántica.
*Criterios de Aceptación:*
[ ] Indexación correcta de documentos.

**Historia 4.3.2: Agente LangChain/LangGraph (Memoria)**
**Pts: 8** | **Asignado a: David (AI Engineer)**
Yo como AI Engineer necesito dotar de razonamiento iterativo (ReAct) al chatbot.
*Criterios de Aceptación:*
[ ] El bot responde citando casos reales.
[ ] Memoria de sesión funcional mediante LangGraph.

---

# 🚀 RELEASE 3: Enterprise Scale (Visión a Largo Plazo)
*Objetivo:* Soportar miles de peticiones bancarias por segundo y análisis en tiempo real.

### 🟦 5.1 Infraestructura Distribuida (Rol: Cloud Architect / DevOps)
**Historia 5.1.1: Dockerización de Servicios**
**Pts: 5** | **Asignado a: Boris (DevOps)**
Yo como DevOps necesito meter todo el monolito en contenedores Docker.
*Criterios de Aceptación:*
[ ] Dockerfiles y Docker Compose funcionales sin errores de entorno.

**Historia 5.1.2: Migración a Kubernetes (K8s)**
**Pts: 8** | **Asignado a: Boris (Cloud Architect)**
Yo como Cloud Architect necesito levantar un cluster (Minikube o EKS) para orquestar los contenedores.
*Criterios de Aceptación:*
[ ] Auto-scaling (HPA) configurado basándose en CPU.

### 🟦 5.2 Streaming en Tiempo Real (Rol: Data Engineer)
**Historia 5.2.1: Setup Apache Kafka Cluster**
**Pts: 5** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito un broker de mensajería (Kafka/RabbitMQ) para los flujos.
*Criterios de Aceptación:*
[ ] Zookeeper y Kafka levantados.

**Historia 5.2.2: Producers y Consumers (Scraping Continuo)**
**Pts: 8** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito que el scraper actúe como un Producer enviando reseñas 24/7.
*Criterios de Aceptación:*
[ ] Ingesta continua en tiempo real sub-segundo en lugar de Batch diario.
