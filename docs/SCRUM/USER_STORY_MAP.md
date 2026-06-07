# Mapa de Historias de Usuario (Product Roadmap)

Este mapa define la visión a corto, mediano y largo plazo del producto B2B SaaS.

> **Leyenda de Puntos de Historia (Pts):** 
> Basado en la sucesión de Fibonacci, mapeado a horas de trabajo asumiendo 1 persona:
> *   `3 Pts`: ~ 4 horas (Medio día)
> *   `5 Pts`: ~ 8 horas (1 día completo)
> *   `8 Pts`: ~ 12-16 horas (1.5 a 2 días)
> *   `13 Pts`: ~ 24+ horas (3+ días - Tarea muy compleja)

---

## 🚀 RELEASE 1: MVP (Mínimo Producto Viable - Presentación Universitaria)
*Objetivo:* Demostrar el valor econométrico y de IA usando datos reales de tiendas de aplicaciones.

### 🟦 1.1 Scraping Básico (Rol: Data Engineer)
**Historia 1.1.1: Ingesta de Datos - PlayStore y AppStore**
**Pts: 8** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito un scraper en PySpark que extraiga reseñas de las tiendas de apps de forma que podamos popular la capa Bronze.
*Criterios de Aceptación:*
[ ] Código PySpark usando `google_play_scraper`.
[ ] Idempotencia (no duplicar reseñas).

### 🟦 1.2 Data Science y Econometría Core (Rol: Econometrista / MLOps)
**Historia 1.2.1: Modelo Probit/Logit de Riesgo de Fuga y NPS**
**Pts: 13** | **Asignado a: Boris (Econometrista)**
Yo como Econometrista necesito calcular el NPS y modelar el *Churn* de forma que podamos alertar al banco sobre fallos críticos.

**Historia 1.2.2: Cadenas de Markov de Satisfacción**
**Pts: 8** | **Asignado a: Boris (Econometrista)**
Yo como Econometrista necesito modelar la matriz de transición de los usuarios.

**Historia 1.2.3: Clasificador NLP Base**
**Pts: 13** | **Asignado a: David (Data Scientist)**
Yo como Científico de Datos necesito un modelo NLP de sentimiento e intención.

### 🟦 1.3 UI/UX y Orquestación (Rol: UI/UX Engineer)
**Historia 1.3.1: Streamlit Dashboard (Patrón F)**
**Pts: 8** | **Asignado a: Boris (UI/UX Engineer)**
Yo como UI/UX Engineer necesito diseñar el Dashboard (Patrón F) mostrando NPS y riesgo de fuga.

**Historia 1.3.2: Menú Interactivo CLI (Capa 4)**
**Pts: 8** | **Asignado a: David (Desarrollador)**
Yo como Desarrollador necesito un menú CLI interactivo (`rich`) para orquestar el MVP.

---

## 🚀 RELEASE 2: B2B SaaS & Omnicanalidad (Comercialización)
*Objetivo:* Expandir la ingesta a todas las redes y crear la API para vender el servicio.

### 🟦 2.1 Scraping Universal y Gobernanza (Rol: Data Engineer)
**Historia 2.1.1: Ingesta Redes (TikTok, IG, FB, X, Trustpilot, Reddit)**
**Pts: 13** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito scrapers del Patrón Strategy para la Voz del Cliente omnicanal.

**Historia 2.1.2: Pipeline de Anonimización (ISO 27001)**
**Pts: 5** | **Asignado a: Boris (Data Engineer)**
Yo como Data Engineer necesito aplicar hashing SHA-256 a PII.

### 🟦 2.2 Banking as a Service (Rol: Backend / AI Engineer)
**Historia 2.2.1: FastAPI B2B Endpoint**
**Pts: 13** | **Asignado a: David (Backend Engineer)**
Yo como Backend Engineer necesito exponer los modelos en una API REST Swagger.

**Historia 2.2.2: Agente LangChain/LangGraph (RAG)**
**Pts: 13** | **Asignado a: David (AI Engineer)**
Yo como AI Engineer necesito un RAG conversacional con estado (LangGraph).

---

## 🚀 RELEASE 3: Enterprise Scale (Visión a Largo Plazo)
*Objetivo:* Soportar miles de peticiones bancarias por segundo y análisis en tiempo real.

### 🟦 3.1 Infraestructura Distribuida (Rol: Cloud Architect)
**Historia 3.1.1: Migración a Kubernetes (K8s)**
**Pts: 13** | **Asignado a: Boris (Cloud Architect)**
Yo como Cloud Architect necesito migrar el monolito a microservicios en K8s de forma que soporte auto-scaling.

**Historia 3.1.2: Streaming de Datos (Kafka)**
**Pts: 13** | **Asignado a: David (Data Engineer)**
Yo como Data Engineer necesito reemplazar el scraping Batch por Apache Kafka de forma que analicemos quejas en Tiempo Real sub-segundo.
