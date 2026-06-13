# Resumen Teórico: Introducción a la Econometría (James Stock & Mark Watson)
*Aplicabilidad al Proyecto OmniVoC SaaS*

Este documento consolida la fundamentación de Stock y Watson para respaldar nuestro modelado longitudinal y longitudinal causal, particularmente para el cálculo del NPS temporal.

## 1. Regresión con Datos de Panel (Panel Data)
La banca móvil cambia a través del tiempo con cada actualización de software, y las reseñas de las tiendas de aplicaciones se comportan como datos agrupados (entidades a lo largo del tiempo). 

### Aplicación al Net Promoter Score (NPS) Longitudinal
En lugar de tomar un promedio estático, el modelo considerará "Entidades" (los diferentes Bancos: BNB, BCP, BancoSol) observados en "Tiempos" diferentes (meses o años de actualización de la App).
*   **Efectos Fijos (Fixed Effects):** Usaremos regresión de efectos fijos de entidad para controlar las variables inobservables que no cambian en el tiempo. Por ejemplo, el "prestigio de marca" histórico de un banco que afecta su NPS base independientemente de si la App falla o no.
*   **Efectos Temporales (Time Effects):** Para controlar choques macroeconómicos o regulaciones de la ASFI que afecten temporalmente a todos los bancos por igual (y sus respectivas reseñas).

## 2. Regresión con Variable Dependiente Binaria y Efectos Marginales
Stock y Watson hacen especial énfasis en la interpretación de los **Efectos Marginales** en modelos no lineales (Probit/Logit).
*   **Impacto no constante:** A diferencia del modelo de regresión lineal, el impacto de una variable (ej. reducir la tasa de fallos de la App en 1%) sobre el Riesgo de Fuga (Churn) dependerá del estado actual del cliente.
*   **Aplicación de Negocio:** Este fundamento nos permitirá construir el Dashboard de Streamlit para simular escenarios: ¿Cuánto decrece la probabilidad de Churn si un banco pasa de un NLP Sentiment neutral a uno positivo, dado que el usuario ya experimentó un fallo grave? Los efectos marginales darán esta respuesta dinámica.

## 3. Amenazas a la Validez Interna y Externa
Stock y Watson proponen un checklist para validar estudios empíricos.
*   **Sesgo de Selección Muestral:** Debemos advertir en los reportes (Business Intelligence) que las reseñas de App Store / Play Store tienen un sesgo hacia los extremos (solo opinan los muy enojados o muy felices). Esto es una amenaza a la validez externa si se generaliza a toda la cartera de clientes de un banco.
