# Arquitectura de Datos y Modelado (Data Architecture & Modeling)

Este documento define la estructura y el viaje de los datos a lo largo de nuestro ecosistema, garantizando rendimiento, trazabilidad histórica y cumplimiento de los requerimientos analíticos B2B.

## 1. Diseño Conceptual: El Flujo Medallón y DAG (Directed Acyclic Graph)

El viaje del dato sigue el paradigma ELT (Extract, Load, Transform), estructurado en tres grandes capas de madurez y orquestado mediante un DAG para garantizar la secuencialidad de las dependencias.

> [!NOTE]
> **OLAP vs OLTP:** Esta arquitectura Medallón (con DuckDB/Parquet) es un motor **OLAP (Online Analytical Processing)** diseñado exclusivamente para lecturas masivas. Las operaciones transaccionales de usuarios SaaS y facturación (OLTP) se separarán en una base PostgreSQL dedicada con RLS (Row Level Security).

```mermaid
graph LR
    %% Sources
    subgraph Internet[Fuentes de Datos]
        A(Play Store)
        B(App Store)
        C(Redes Sociales)
    end

    %% Capa Bronze
    subgraph Bronze[Bronze Layer - Raw/Ingestion]
        D[(Datos Crudos<br/>JSON/Parquet)]
        H{Hashing PII<br/>Privacy by Design}
    end

    %% Capa Silver
    subgraph Silver[Silver Layer - Cleansed/Conformed]
        E[(Datos Limpios<br/>Pydantic Validated)]
        Q{Data Quality<br/>Observability}
    end

    %% Capa Gold
    subgraph Gold[Gold Layer - Analytics]
        F[(Star Schema<br/>BI Ready)]
    end

    %% NLP Models
    subgraph ML[Modelos ML / NLP]
        M(Análisis de Sentimiento)
        N(Clasificación de Temas)
    end

    %% Dashboard
    O[[Streamlit Dashboard]]

    Internet -- Extract --> H
    H -- Load --> D
    D -- Limpieza Básica --> Q
    Q -- Transform --> E
    E -- Inferencia --> ML
    ML -- Enriquecimiento --> E
    E -- Agregación Dimensional --> F
    F -- Consultas SQL Rápidas --> O
```

---

## 2. Diseño Lógico: Diagrama Entidad-Relación (DER)

A nivel lógico, antes de pensar en tablas analíticas, nuestro dominio de negocio se entiende mediante las siguientes relaciones abstractas entre entidades clave.

```mermaid
erDiagram
    APPLICATION ||--o{ REVIEW : receives
    USER ||--o{ REVIEW : writes
    REVIEW ||--|| SENTIMENT : has
    REVIEW }|..|{ THEME : mentions

    APPLICATION {
        string AppName
        string Category
        string Platform
    }
    USER {
        string HashID
        string Location
    }
    REVIEW {
        string Content
        int Rating
        datetime Date
    }
    SENTIMENT {
        string Label
        float Score
    }
    THEME {
        string TopicName
    }
```

---

## 3. Diseño Físico: Star Schema en Capa Gold (DuckDB / Parquet)

Para maximizar el rendimiento del Dashboard, la capa Gold se estructura usando un **Esquema de Estrella (Star Schema)**. Además, implementamos **Slowly Changing Dimensions (SCD) Tipo 2** en dimensiones críticas (como `Dim_App`) para preservar la historia de los cambios (ej. si una app cambia de categoría, no queremos reescribir el pasado).

```mermaid
erDiagram
    Fact_Reviews }|--|| Dim_App : "app_sk"
    Fact_Reviews }|--|| Dim_Date : "date_sk"
    Fact_Reviews }|--|| Dim_Sentiment : "sentiment_sk"
    Fact_Reviews }|--|| Dim_User : "user_sk"

    Fact_Reviews {
        bigint review_id PK
        int app_sk FK
        int date_sk FK
        int sentiment_sk FK
        string user_sk FK
        float nps_contribution
        boolean is_churn_risk
        int rating
    }

    Dim_App {
        int app_sk PK "Surrogate Key"
        string app_id "Natural Key (Bundle ID)"
        string app_name
        string category
        string platform
        date valid_from "SCD2: Inicio de Vigencia"
        date valid_to "SCD2: Fin de Vigencia"
        boolean is_current "SCD2: Flag Activo"
    }

    Dim_Date {
        int date_sk PK "Ej: 20260611"
        date full_date
        int year
        int month
        int day
        string day_of_week
        boolean is_weekend
    }

    Dim_Sentiment {
        int sentiment_sk PK
        string sentiment_label "Positivo, Neutral, Negativo"
        float confidence_score_avg
    }

    Dim_User {
        string user_sk PK "Hash SHA-256"
        string location_proxy "Deducido de metadata"
        boolean is_verified
    }
```

### Especificaciones de Ingeniería Adicionales

1. **Estrategia de Particionamiento (Partitioning):**
   Los archivos Parquet de las tablas de hechos (`Fact_Reviews`) y la capa Silver estarán particionados físicamente por `year/month/`. Esto permite que DuckDB aplique *Partition Pruning*, leyendo solo los archivos del mes consultado, lo que reduce drásticamente el consumo de RAM y el tiempo de I/O.

2. **SCD Tipo 2 (Slowly Changing Dimensions):**
   Como se observa en `Dim_App`, utilizamos claves subrogadas (Surrogate Keys, `app_sk`). Si la aplicación cambia de nombre o categoría, se inserta una nueva fila en `Dim_App` con un nuevo `app_sk`, se cierra la fecha `valid_to` del registro anterior y se marca `is_current = false`.

3. **Data Quality Gates & Observability:**
   La transición de Bronze a Silver no es automática. Se ejecutarán "Compuertas" (**Data Quality Checks**) en los pipelines que validen esquemas y calidad (Ej. rechazar un registro si un campo clave viene nulo). El objetivo es evitar que la información errónea corrompa la capa Silver.

4. **Cifrado en Tránsito y Reposo (ISO 27001):**
   Todo dato en tránsito viaja usando protocolos seguros (HTTPS/TLS). Los archivos Parquet de la capa Bronze en reposo estarán cifrados usando KMS (AES-256) garantizando la confidencialidad.

5. **Carga Incremental y CDC (Change Data Capture):**
   A medida que el volumen escale, el pipeline evolucionará hacia una arquitectura CDC para inyectar solo los registros nuevos o modificados, manteniendo un registro auditable del **Data Lineage** para certificar la procedencia de cada fila en la capa Gold.
