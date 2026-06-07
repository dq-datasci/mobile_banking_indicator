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

## 🟧 ACTIVIDAD 2: Modelado Analítico (IA, ML y Econometría)

### 🟦 2.1 Análisis de Sentimiento (NLP)
**Historia 2.1.1: Clasificador NLP**
**Pts: 13** | **Asignado a: David**
Yo como Analista necesito aplicar un modelo de procesamiento de lenguaje natural (HuggingFace/Transformers) a los textos de forma que pueda etiquetar cada reseña como Positiva, Negativa o Neutra.
*Criterios de Aceptación:*
[ ] Modelo integrado y corriendo sobre los datos "Silver".
[ ] Tracking de los experimentos y precisión usando MLflow.
[ ] Identificación y extracción de "Fallas Técnicas" vs "Quejas de Servicio".

### 🟦 2.2 Modelado Econométrico
**Historia 2.2.1: Modelo Probit/Logit**
**Pts: 13** | **Asignado a: Boris**
Yo como Economista necesito correr un modelo de elección discreta (Logit/Probit) de forma que se estime la probabilidad de insatisfacción crítica basándose en variables como [frecuencia de caída de app, lentitud, error de token].
*Criterios de Aceptación:*
[ ] Estimación del modelo en Quarto (R/Python).
[ ] Validación de supuestos estadísticos (ej. Heterocedasticidad).
[ ] Resultados exportados a la capa "Gold" para visualización.

---

## 🟧 ACTIVIDAD 3: Optimización y Dashboard (BI & Scrum)

### 🟦 3.1 Orquestación y CLI Interactiva
**Historia 3.1.1: Menú Interactivo (Capa 4)**
**Pts: 8** | **Asignado a: David**
Yo como Desarrollador necesito un menú CLI interactivo (usando la librería `rich`) de forma que pueda orquestar las ejecuciones (scraping, ML, dashboard) sin ejecutar comandos largos, manteniendo idempotencia.
*Criterios de Aceptación:*
[ ] Interfaz de consola hermosa y profesional.
[ ] Menú con opciones enumeradas (Ej: 1. Extraer Datos, 2. Entrenar Modelo, 3. Dashboard).
[ ] Manejo robusto de errores (try/except) sin crashear.

**Historia 3.1.2: Bot RAG de Consultas**
**Pts: 8** | **Asignado a: David**
Yo como Gerente del Banco necesito un asistente conversacional (LangChain RAG) integrado al proyecto de forma que pueda hacer preguntas en lenguaje natural sobre las reseñas de los clientes.
*Criterios de Aceptación:*
[ ] Base de datos vectorial configurada localmente.
[ ] Agente LangChain capaz de responder preguntas citando reseñas reales.

### 🟦 3.2 Visualización Final
**Historia 3.2.1: Dashboard Streamlit**
**Pts: 8** | **Asignado a: Boris**
Yo como Tomador de Decisiones necesito un Dashboard interactivo de forma que pueda visualizar la evolución del indicador sintético de calidad (2023-2026).
*Criterios de Aceptación:*
[ ] App en Streamlit funcional.
[ ] Gráficos en Plotly mostrando la evolución de sentimiento y las cadenas de Markov.
[ ] Interfaz limpia, intuitiva y rápida.
