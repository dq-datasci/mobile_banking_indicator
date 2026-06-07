# Registro de Decisiones Diferidas y Funcionalidades Pausadas (Deferred Features)

En un proyecto de grado corporativo B2B SaaS, muchas veces surgen excelentes ideas arquitectónicas que, por limitaciones de tiempo para un MVP (Minimum Viable Product), deben pausarse o diferirse para versiones futuras. 

Este documento rastrea todas las decisiones tecnológicas o features que **hemos decidido conscientemente NO implementar en el Sprint actual**, junto con su justificación. Nada se pierde, todo se documenta.

---

## 1. Kubernetes y Arquitectura de Microservicios Distribuidos
*   **Decisión:** Pausado. El sistema operará como un Monolito Modular.
*   **Justificación:** Demasiada sobrecarga (overhead) de DevOps para un equipo de 2 personas en un MVP. Añadiría latencia de red y requeriría clusters costosos (EKS/GKE). El Monolito Modular nos da la limpieza de código necesaria sin la complejidad operativa.

## 2. Aplicación Móvil / Escritorio Nativa
*   **Decisión:** Pausado. Todo se desplegará en entorno Web (Streamlit/FastAPI).
*   **Justificación:** Un dashboard analítico con complejas tablas de datos y gráficos econométricos requiere una pantalla grande para aplicar correctamente el Patrón F de UX. Empaquetar esto en Android/iOS arruinaría la experiencia de usuario de un ejecutivo.

## 3. Streaming de Datos en Tiempo Real (Kafka/RabbitMQ)
*   **Decisión:** Pausado. El pipeline será de procesamiento Batch (Lotes).
*   **Justificación:** Las reseñas de las tiendas de apps y redes sociales no requieren análisis de latencia sub-segundo (como la detección de fraude en tarjetas). Ejecutar un cronjob diario o un Menú CLI bajo demanda es 100% suficiente para calcular el NPS y el Churn.

## 4. MCP (Model Context Protocol) para Múltiples LLMs concurrentes
*   **Decisión:** Diferido. Se usará LangChain/LangGraph con un solo LLM poderoso (ej. OpenAI o Gemini) inicialmente.
*   **Justificación:** Implementar múltiples agentes que debatan entre sí con distintos LLMs es brillante, pero para la primera iteración del RAG, un solo agente con buena memoria (LangGraph) cumple el objetivo con menos latencia.
