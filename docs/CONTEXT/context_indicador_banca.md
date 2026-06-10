# Contexto del Proyecto: Construcción de un Indicador Sintético

Este documento resume los puntos clave extraídos de la investigación original y sirve como contexto base para el desarrollo del proyecto integrador (7 materias).

## 1. Problema a Resolver
Aunque la banca móvil ha crecido en Bolivia, los bancos carecen de herramientas para procesar las reseñas (comentarios, quejas) en tiempo real para evaluar cuantitativamente la Calidad Percibida (UX).

## 2. Objetivos del Proyecto
Construir un **Indicador Sintético** que evalúe la calidad de la banca móvil en Bolivia empleando NLP y ML.
*   Extraer reseñas de App Store / Play Store.
*   Procesar semánticamente los textos.
*   Clasificar los tipos de comentarios.
*   Visualizar en un Dashboard interactivo.

## 3. Matriz de Integración de Materias

| Materia | Implementación en el Proyecto |
| :--- | :--- |
| **Metodología de la Investigación** | Estructuración, diseño longitudinal, justificación (basado en el Docx original). |
| **Ingeniería de Datos** | Pipeline ETL: Extracción y limpieza masiva usando **PySpark** y **Databricks**. |
| **Inteligencia Artificial y ML I** | Modelos de NLP para clasificar sentimiento de comentarios en texto no estructurado. Tracking con **MLflow**. |
| **Business Intelligence I** | Creación del **Dashboard interactivo en Streamlit** para visualizar KPIs. |
| **Modelización Empresarial II (Econometría)** | Aplicación de Modelos de Corte Transversal (**Logit/Probit**) para predecir la probabilidad de queja de un usuario según fallos técnicos. |
| **Optimización Empresarial II** | Uso de **Cadenas de Markov** para modelar la probabilidad de transición entre estados de usuario (Ej: Satisfecho -> Queja -> Fuga). |
| **Sistemas Integrados de Gestión** | Diseño del indicador sintético como métrica para procesos de mejora continua alineados a **ISO 9001**. |
