# Modelo de Negocio y Propuesta de Valor (Voice of Customer AI)

## 1. El Problema que Resolvemos
Las corporaciones (Bancos, Fintechs, E-Commerce, Retail) invierten millones de dólares en marketing para adquirir usuarios, pero sufren una pérdida silenciosa y constante: el **Churn (Fuga de Clientes)**. 
Actualmente, los gerentes leen reseñas aleatorias de la Play Store o ven un "promedio de 3 estrellas", pero no tienen forma de saber:
1. ¿Qué porcentaje exacto de esas quejas se debe a un error técnico vs mala atención al cliente?
2. ¿Qué error técnico está causando la mayor probabilidad de fuga inmediata?
3. ¿Cuál es el impacto financiero de no arreglar el problema X?

## 2. Nuestra Solución (El Producto)
**Voice of Customer AI (VoC-AI)** es un producto B2B SaaS que consolida la voz del usuario a través del internet entero, aplica Inteligencia Artificial y devuelve *insights* accionables.
No es un simple dashboard de "sentimiento". Es un **motor econométrico**. Te dice: *"El 40% de las quejas en TikTok y Play Store son sobre biometría facial. Arreglar esto reducirá el riesgo de fuga en un 18%"*.

## 3. Omnicanalidad (Ingesta de Datos Universales)
El valor del producto reside en que las quejas no solo ocurren en la tienda de aplicaciones. Un usuario muy enojado se queja en Twitter. Un usuario frustrado hace un TikTok.
Por lo tanto, extraeremos datos masivos de:
*   **Tiendas Oficiales:** Google Play Store, Apple App Store.
*   **Redes de Difusión:** X (Twitter), Facebook, Instagram, TikTok.
*   **Foros y Reseñas:** Reddit, Trustpilot.

## 4. Monetización y Despliegue
*   **Costo de Desarrollo (Prototipo/MVP):** $0. Despliegue en Streamlit Community Cloud + Base de Datos embebida local (DuckDB).
*   **Venta Enterprise (Modelo BaaS - Backend as a Service):** Si una empresa quiere comprar la tecnología, le vendemos acceso a nuestra **FastAPI**. El costo de infraestructura lo minimizamos usando arquitectura *Serverless* (Pago por uso en AWS Lambda o Ubicloud), logrando márgenes de ganancia superiores al 80%.
