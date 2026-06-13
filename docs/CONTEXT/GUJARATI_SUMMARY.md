# Resumen Teórico: Econometría (Damodar N. Gujarati - 5ta Ed.)
*Aplicabilidad al Proyecto OmniVoC SaaS*

Este documento consolida la fundamentación matemática extraída del libro de Gujarati para respaldar la **Historia 2.2.1 (Modelo Logit Riesgo Churn)**.

## 1. Modelos de Regresión de Respuesta Cualitativa (Logit y Probit)
En nuestro proyecto, la variable dependiente (Churn/Fuga) es binaria (1 = El cliente se va, 0 = El cliente se queda). Gujarati establece que el Modelo Lineal de Probabilidad (MLP) es inadecuado porque puede generar probabilidades menores a 0 o mayores a 1.

### Aplicación: Modelo Logit (Regresión Logística)
Para la Historia 2.2.1, utilizaremos la función de distribución acumulada (FDA) logística.
*   **Variable Dependiente ($Y_i$):** Probabilidad de Churn.
*   **Variables Independientes ($X_i$):** Sentimiento del NLP (negativo), menciones de fallos en biometría, etc.
*   **Odds Ratio (Razón de Probabilidades):** Nos permitirá interpretar el impacto. Por ejemplo, calcular matemáticamente que un fallo de "Biometría" (X=1) multiplica por 3.5 los *Odds* de abandonar el banco en comparación a un fallo estético.

### Aplicación: Modelo Probit
Alternativa matemática que asume una distribución normal estándar. Por patrón *Strategy*, implementaremos ambos en Scikit-Learn/Statsmodels para comparar el pseudo-$R^2$ de McFadden y la tasa de falsos negativos (vital para no ignorar clientes en riesgo).

## 2. Relajación de Supuestos (Heterocedasticidad y Multicolinealidad)
Para garantizar la fiabilidad del modelo (*Reliability* en ISO 25010), debemos testear las siguientes violaciones clásicas:

### Multicolinealidad
Gujarati advierte sobre variables explicativas altamente correlacionadas.
*   **Riesgo en nuestro pipeline:** Si incluimos la variable de "Calificación en Estrellas" y la variable de "Sentimiento NLP", es probable que sufran multicolinealidad perfecta o imperfecta grave. Esto inflaría los errores estándar.
*   **Mitigación:** Aplicar Factor de Inflación de Varianza (VIF) antes del entrenamiento del modelo Logit.

### Heterocedasticidad
*   **Riesgo en nuestro pipeline:** La varianza de las quejas puede cambiar según el banco. Los bancos grandes pueden tener patrones de error con mayor varianza que los pequeños.
*   **Mitigación:** Utilizar errores estándar robustos (White) en la librería `statsmodels` al entrenar el Logit.
