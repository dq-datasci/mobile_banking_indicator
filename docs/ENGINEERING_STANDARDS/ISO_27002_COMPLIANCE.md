# Cumplimiento del Estándar ISO/IEC 27002:2022

Este documento condensa los controles de seguridad de la información aplicables a **OmniVoC SaaS** extraídos de la norma ISO/IEC 27002:2022. Estos lineamientos rigen el ciclo de vida del desarrollo y la protección de datos dentro de nuestra Arquitectura Medallón.

## 1. Controles Organizacionales

*   **5.8 Information security in project management:** La seguridad de la información debe integrarse en todas las fases del ciclo de vida del proyecto. Todas las historias de usuario deben evaluarse bajo este criterio antes de ser desarrolladas.
*   **5.10 Acceptable use of information:** Se deben establecer políticas claras para el manejo de activos de información y los datos scrapeados de las redes sociales.
*   **5.14 Information transfer:** Toda transferencia de datos (ej. desde las APIs de terceros hacia la capa Bronze) debe estar protegida para garantizar la confidencialidad e integridad, requiriendo el uso de canales cifrados.
*   **5.20 Addressing information security within supplier agreements:** Al interactuar con proveedores o plataformas de terceros (como las tiendas de aplicaciones), es necesario considerar los términos de servicio, rate-limits y seguridad de la información intercambiada.
*   **5.34 Privacy and protection of PII:** La privacidad es obligatoria por diseño. Cualquier Información Personal Identificable (PII) recolectada debe ser anonimizada antes de su persistencia en el Lakehouse, cumpliendo estrictamente con legislaciones aplicables.

## 2. Controles Tecnológicos

*   **8.11 Data masking:** El enmascaramiento de datos es un pilar fundamental en nuestro procesamiento. Aplicaremos funciones hash (SHA-256) u ofuscación en la ingesta (capa Bronze) para proteger nombres de usuario y perfiles, mitigando la exposición de PII.
*   **8.24 Use of cryptography:** Todos los datos confidenciales en tránsito y en reposo deben estar debidamente protegidos mediante cifrado.
*   **8.28 Secure coding:** La escritura de código debe regirse por pautas seguras para prevenir inyecciones, fugas de memoria o vulnerabilidades sistémicas. Se usarán herramientas como `ruff` y hooks de `pre-commit` para análisis estático constante.
*   **8.31 Separation of development, test and production environments:** Mantendremos los ambientes de desarrollo, pruebas y producción estrictamente separados para prevenir la corrupción de datos y el acceso no autorizado a la infraestructura operativa.
