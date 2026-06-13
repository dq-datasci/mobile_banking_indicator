# Conclusiones del Análisis Exploratorio (EDA) - Capa Silver

Este reporte sintetiza los hallazgos tras la ejecución del EDA híbrido (PySpark + `ydata-profiling`) sobre el Lakehouse de OmniVoC.

## 1. Hallazgos Generales (Motor Distribuido PySpark)
El dataset analizado contiene **59,795 reseñas verificadas** correspondientes a 8 bancos bolivianos.

### Distribución por Institución Financiera (Top 3)
| Banco | Reseñas | Porcentaje |
|---|---|---|
| **Banco de Crédito (BCP)** | 17,463 | 29.2% |
| **Banco Unión** | 14,376 | 24.0% |
| **Banco Ganadero** | 8,593 | 14.3% |

### Estadísticas de Calificaciones (Rating)
*   **Media Global:** 3.08
*   **Desviación Estándar:** 1.85
*   **Rango:** [1, 5]

> [!WARNING]
> La altísima desviación estándar (1.85) sobre un rango de 1 a 5 indica que las reseñas están **extremadamente polarizadas**: los usuarios tienden a puntuar con 5 estrellas o con 1 estrella, sin términos medios. Hay un **riesgo altísimo de Churn explícito** en la base de datos.

### Análisis de Calidad y Faltantes (Missing Values)
*   **Contenido de reseña (`content`):** 0% nulos. La limpieza en Silver fue exitosa.
*   **Respuestas del banco (`replyContent`):** 68.5% nulos. 

> [!TIP]
> Solo el 31.5% de los clientes reciben atención al cliente o respuesta tras dejar una queja en las tiendas de aplicaciones. Esta "ausencia de respuesta" es un driver comprobado de abandono.

## 2. Hallazgos Específicos: Banco de Crédito (BCP)
Mediante la ejecución aislada de `ydata-profiling` sobre la muestra del BCP, confirmamos:
*   Una correlación fuerte entre versiones específicas de la app **Yape** y los picos de quejas de 1 estrella.
*   Presencia cíclica de fricciones relacionadas con transacciones "pendientes" o caídas a fin de mes.

## 3. Siguientes Pasos y Propuestas Técnicas
Para habilitar la **Historia 2.2.1** (Modelo de Riesgo Logit) en el Pipeline Gold, recomiendo implementar los siguientes pasos técnicos (Feature Engineering):

1. **Definición de Variable Proxy para Churn:**
   *   Crear una variable binaria objetivo `is_churn_risk`: `1` si `Rating <= 2`, `0` en otro caso.

2. **Ingeniería de Características Comportamentales:**
   *   Crear indicador binario `has_bank_reply`: `1` si `replyContent` no es nulo.
   *   Calcular la métrica `content_length` (longitud del texto de queja). Los clientes insatisfechos suelen redactar textos mucho más largos; esto puede ser un fuerte regresor para el modelo Logit.
   *   Extraer `hour_of_day` desde el campo `at` para detectar quejas de madrugada asociadas a fallos de infraestructura bancaria nocturna.

3. **Imputación de Valores Desconocidos:**
   *   Para las variables `appVersion` y `reviewCreatedVersion` nulas, reemplazarlas explícitamente con el token `"UNKNOWN"` para no perder las filas en las regresiones.

4. **Cálculo de NPS (Net Promoter Score):**
   *   Re-clasificar numéricamente para la Historia 2.2.2: Promotores (5), Pasivos (4,3), Detractores (2,1).

> [!IMPORTANT]
> Se actualizará el contrato de datos `gold_contracts.py` y `gold_pipeline.py` para incluir estas nuevas variables categóricas y numéricas derivadas, dejándolas listas para el modelo MLOps con `statsmodels` y `PyCaret`.
