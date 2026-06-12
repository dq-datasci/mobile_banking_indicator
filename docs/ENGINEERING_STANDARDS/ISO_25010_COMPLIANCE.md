# Cumplimiento del Estándar ISO/IEC 25010:2023 (Modelo de Calidad del Producto)

Este documento condensa los lineamientos y métricas de calidad de software extraídos de la norma **ISO/IEC 25010:2023**, adaptados a nuestra arquitectura DevOps y ciclo de vida de desarrollo. Este estándar es el principal marco de referencia para asegurar que OmniVoC SaaS entregue valor de manera consistente, segura y confiable.

## 1. Las 9 Características de Calidad de ISO 25010:2023

El modelo actualizado divide la calidad del producto en nueve características fundamentales. A continuación, se detalla cómo las abordamos desde una perspectiva DevOps:

### 1.1. Functional Suitability (Adecuación Funcional)
Garantiza que el software cumple con los requisitos del negocio.
*   **Completeness, Correctness, Appropriateness:** Se logrará mediante pruebas automatizadas exhaustivas (Unitarias y de Integración) ejecutadas en los pipelines de GitHub Actions antes de cada *merge* a `develop`.

### 1.2. Performance Efficiency (Eficiencia de Desempeño)
Garantiza que el sistema gestione la carga de trabajo eficientemente.
*   **Time behaviour & Resource utilization:** Monitoreo activo de DuckDB y PySpark. Uso de auto-scaling y orquestación de contenedores en la nube para adaptarse dinámicamente a picos de demanda.

### 1.3. Compatibility (Compatibilidad)
Garantiza la integración en ecosistemas diversos.
*   **Co-existence & Interoperability:** Aislamiento mediante contenedores (Docker) y estandarización de comunicación vía APIs RESTful (FastAPI), garantizando que nuestros servicios coexistan sin conflictos.

### 1.4. Interaction Capability (Capacidad de Interacción)
Reemplaza al antiguo "Usability". Se enfoca en que los usuarios puedan interactuar efectivamente con el sistema.
*   **Inclusivity & Error Protection:** Despliegues *self-service* y tableros automatizados. En el Dashboard de Streamlit, se aplicarán jerarquías visuales claras y manejo de errores proactivo para evitar que los gerentes interpreten mal los datos econométricos.

### 1.5. Reliability (Fiabilidad)
Asegura que el sistema funcione consistentemente bajo diversas condiciones.
*   **Maturity, Fault tolerance, Recoverability:** Implementación de Rollbacks automáticos, arquitecturas tolerantes a fallos y copias de seguridad continuas para asegurar una rápida recuperación (alineado con nuestro RTO en el BIA).

### 1.6. Security (Seguridad)
Protege la información contra accesos no autorizados y modificaciones.
*   **Confidentiality, Integrity, Non-repudiation:** Integración de herramientas DevSecOps en el pipeline. Hashing de PII mediante contratos de Pydantic, análisis de vulnerabilidades automatizado y registros (Logs) inmutables para trazabilidad.

### 1.7. Maintainability (Mantenibilidad)
Permite modificaciones y actualizaciones sin riesgo sistémico.
*   **Modularity, Reusability, Analysability:** Arquitectura basada en microservicios lógicos (Monolito Modular), *Infrastructure as Code* (Terraform) y registro centralizado (`AuditLogger`) para un fácil análisis de causa raíz.

### 1.8. Flexibility (Flexibilidad)
Reemplaza "Portability". Facilita la adaptación a nuevos entornos y escalas.
*   **Adaptability & Scalability:** Arquitecturas *cloud-agnostic* y metodologías de escalamiento dinámico (Kubernetes), asegurando que el despliegue del sistema pueda transicionarse suavemente de un proveedor cloud a otro sin reescrituras masivas.

### 1.9. Safety (Seguridad Física / Operativa - Nueva Característica)
Garantiza que el sistema se recupere de fallos de infraestructura sin causar daños al negocio.
*   **Operational Constraint & Fail Safe:** Mecanismos *Fail-safe* implementados, diseño de ingeniería del caos (Chaos Engineering), y validaciones automatizadas de resiliencia antes de cada despliegue a producción.

## 2. Métricas y Aseguramiento de Calidad Continua

El cumplimiento de este estándar no es una actividad de un solo paso, sino que se valida de manera continua en nuestro entorno DevOps a través de *Quality Gates*:
1.  **Shift-left testing:** Las aserciones de seguridad y rendimiento se prueban desde el entorno local.
2.  **Continuous Monitoring:** Observabilidad en tiempo real para métricas de *Performance* y *Reliability*.
3.  **Continuous Delivery:** Actualizaciones frecuentes sin tiempo de inactividad, mejorando la *Maintainability*.
