# Mapa de Historias de Usuario (User Story Map)

Este mapa organiza el proyecto de forma visual jerárquica (Épicas -> Features -> Historias de Usuario), preparado para dividirse en "Releases" o Sprints.

## 🟧 ACTIVIDAD 1: Pipeline de Datos e Ingeniería (PySpark)

### 🟦 1.1 Extracción de Reseñas
**Historia 1.1.1: Scraping Básico**
**Pts: 5** | **Asignado a: David**
Yo como Ingeniero de Datos necesito extraer las reseñas públicas de la Play Store de los principales bancos de Bolivia de forma que tengamos un conjunto de datos crudos para analizar.
*Criterios de Aceptación:*
[ ] Código en PySpark capaz de extraer al menos 5,000 reseñas.
[ ] Se guardan los datos en formato Parquet o CSV en la capa "Bronze" de la base de datos (DuckDB local).
[ ] Control de errores para evitar bloqueos por rate-limit.

### 🟦 1.2 Limpieza y EDA
**Historia 1.2.1: Limpieza de Texto**
**Pts: 8** | **Asignado a: Boris**
Yo como Científico de Datos necesito limpiar el texto (eliminar emojis irrelevantes, normalizar modismos bolivianos, corregir ortografía) de forma que el modelo de NLP reciba texto de alta calidad.
*Criterios de Aceptación:*
[ ] Script en PySpark que elimina stop-words y caracteres especiales.
[ ] Creación de un diccionario básico de modismos financieros locales.
[ ] Se guardan los datos limpios en la capa "Silver".

---

## 🟧 ACTIVIDAD 2: Modelado Analítico, Econometría y Optimización

### 🟦 2.1 Inteligencia Artificial (NLP)
**Historia 2.1.1: Clasificador NLP de Sentimiento**
**Pts: 13** | **Asignado a: David**
Yo como Data Scientist necesito un modelo NLP que procese el texto limpio de forma que clasifique el sentimiento (Positivo/Negativo) y extraiga las entidades clave (Login, Token, Transferencia).
*Criterios de Aceptación:*
[ ] Pipeline de MLflow configurado.
[ ] Precisión del modelo superior al 85%.

### 🟦 2.2 Econometría y Procesos Estocásticos
**Historia 2.2.1: Modelo Probit/Logit (Riesgo de Fuga)**
**Pts: 13** | **Asignado a: Boris**
Yo como Analista necesito un modelo Logit usando los datos de reseñas de forma que pueda calcular la probabilidad de que un usuario abandone la app (Churn).
*Criterios de Aceptación:*
[ ] Uso de R o statsmodels en Python.
[ ] Pruebas de Heterocedasticidad superadas.

**Historia 2.2.2: Cadenas de Markov (Transición de Estado)**
**Pts: 8** | **Asignado a: Boris**
Yo como Analista necesito aplicar Cadenas de Markov de forma que pueda predecir cómo un usuario transita de un estado "Satisfecho" a "Frustrado".
*Criterios de Aceptación:*
[ ] Matriz de transición calculada.

---

## 🟧 ACTIVIDAD 3: Optimización, B2B SaaS y Dashboard

### 🟦 3.1 Orquestación y CLI Interactiva
**Historia 3.1.1: Menú Interactivo (Capa 4)**
**Pts: 8** | **Asignado a: David**
Yo como Desarrollador necesito un menú CLI interactivo (usando la librería `rich`) de forma que pueda orquestar las ejecuciones.
*Criterios de Aceptación:*
[ ] Interfaz de consola hermosa.
[ ] Manejo robusto de errores.

### 🟦 3.2 Endpoint Enterprise (B2B SaaS)
**Historia 3.2.1: API REST B2B**
**Pts: 13** | **Asignado a: David**
Yo como CEO del Proyecto necesito que los modelos vivan detrás de una API FastAPI de forma que podamos vender el acceso a bancos externos (Banking as a Service).
*Criterios de Aceptación:*
[ ] Endpoint documentado en Swagger.
[ ] Tiempos de respuesta < 200ms.

### 🟦 3.3 Visualización Final y RAG
**Historia 3.3.1: Dashboard Streamlit**
**Pts: 8** | **Asignado a: Boris**
Yo como Gerente del Banco necesito un dashboard interactivo de forma que pueda ver el Indicador Sintético, el Market Share y consultar a la IA vía RAG.
*Criterios de Aceptación:*
[ ] Gráficas Plotly (Aesthetics BI).
[ ] Asistente RAG LangChain integrado. de sentimiento y las cadenas de Markov.
[ ] Interfaz limpia, intuitiva y rápida.
