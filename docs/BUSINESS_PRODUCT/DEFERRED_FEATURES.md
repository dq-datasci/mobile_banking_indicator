# Registro de Decisiones Diferidas y Funcionalidades Pausadas (Deferred Features)

En un proyecto de grado corporativo B2B SaaS, muchas veces surgen excelentes ideas arquitectónicas que, por limitaciones de tiempo para un MVP (Minimum Viable Product), deben pausarse o diferirse para versiones futuras.

Este documento rastrea todas las decisiones tecnológicas o features que **hemos decidido conscientemente NO implementar en el Sprint actual**, junto con su justificación. Nada se pierde, todo se documenta.

---

## 1. Kubernetes y Arquitectura de Microservicios Distribuidos
*   **Decisión:** Diferido para el **Release 3 (Enterprise Scale)**.
*   **Justificación:** Demasiada sobrecarga (overhead) de DevOps para un equipo de 2 personas en un MVP. El Monolito Modular nos da la limpieza de código necesaria para los Releases 1 y 2.

## 2. Aplicación Móvil / Escritorio Nativa
*   **Decisión:** Pausado Indefinidamente. Todo se desplegará en entorno Web (Streamlit/FastAPI).
*   **Justificación:** Un dashboard analítico con complejas tablas de datos y gráficos econométricos requiere una pantalla grande para aplicar correctamente el Patrón F de UX. Empaquetar esto en Android/iOS arruinaría la experiencia de usuario de un ejecutivo.

## 3. Streaming de Datos en Tiempo Real (Kafka/RabbitMQ)
*   **Decisión:** Diferido para el **Release 3 (Enterprise Scale)**.
*   **Justificación:** Las reseñas de las tiendas de apps y redes sociales no requieren análisis de latencia sub-segundo para el MVP. Ejecutar un Menú CLI bajo demanda es 100% suficiente para calcular el NPS y el Churn temporalmente.

## 4. MCP (Model Context Protocol) para Múltiples LLMs concurrentes
*   **Decisión:** Diferido. Se usará LangChain/LangGraph con un solo LLM poderoso (ej. OpenAI o Gemini) inicialmente.
*   **Justificación:** Implementar múltiples agentes que debatan entre sí con distintos LLMs es brillante, pero para la primera iteración del RAG, un solo agente con buena memoria (LangGraph) cumple el objetivo con menos latencia.

## 5. Capa de Búsqueda (Elasticsearch / OpenSearch)
*   **Decisión:** Diferido para el **Release 4 (Enterprise Deep Listening)**.
*   **Justificación:** Añadir una capa de búsqueda Full-Text hiper-rápida es vital para que clientes B2B puedan buscar quejas específicas entre millones de registros. Sin embargo, configurar y mantener nodos de Elasticsearch en este momento dispararía los costos de nube e introduciría complejidad innecesaria para las validaciones del MVP y Release 2, donde la analítica columnar (DuckDB/Parquet) es suficientemente veloz para los tableros generales.

## 6. Integración del Reporte EDA en Dashboard de Streamlit
*   **Decisión:** Diferido Indefinidamente. El reporte HTML generado por `ydata-profiling` se mantendrá como un artefacto estático local para el Data Analyst.
*   **Justificación:** El reporte contiene marcas de agua y terminología técnica propia de herramientas de calidad de datos. Los clientes B2B (gerentes/ejecutivos) requieren métricas limpias orientadas a valor, por lo que integrar un archivo HTML crudo de este tamaño degradaría la estética y el "Interaction Capability" (ISO 25010) del producto final.
