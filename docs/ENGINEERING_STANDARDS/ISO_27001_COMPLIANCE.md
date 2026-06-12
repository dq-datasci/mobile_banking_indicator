# Cumplimiento del Estándar ISO/IEC 27001:2022

Este documento condensa los requisitos y controles del Sistema de Gestión de Seguridad de la Información (ISMS) aplicables a **OmniVoC SaaS** extraídos de la norma ISO/IEC 27001:2022. Estos lineamientos complementan la ISO 27002 y rigen nuestra gestión de riesgos y desarrollo seguro.

## 1. Sistema de Gestión de Seguridad (ISMS) - Requisitos Core

*   **6.1.2 Information security risk assessment:** Debemos identificar, analizar y evaluar los riesgos de seguridad de la información. En nuestro contexto, esto implica evaluar constantemente el riesgo de extraer basura, fugas de PII, y manipulación de modelos de Machine Learning.
*   **6.1.3 Information security risk treatment:** Todo riesgo identificado debe tener un plan de tratamiento. Usaremos validadores estrictos (Pydantic), y arquitectura Medallón para mitigar el riesgo de corrupción de datos.

## 2. Controles de Seguridad (Annex A)

### A.5 Controles Organizacionales
*   **A.5.15 Access control:** Las reglas de control de acceso lógico y físico deben estar implementadas. Solo el orquestador y los scripts autorizados deben poder tocar la capa Bronze.
*   **A.5.24 Information security incident management:** Debemos tener preparado un plan de respuesta a incidentes (ej. si la API de PlayStore bloquea nuestra IP, o si detectamos una fuga de PII).
*   **A.5.34 Privacy and protection of PII:** Anonimización OBLIGATORIA desde el origen.
*   **A.5.36 Compliance with policies:** El código debe ser revisado regularmente (vía pre-commits y CI/CD) para asegurar que las políticas de seguridad se cumplen.

### A.8 Controles Tecnológicos
*   **A.8.2 Privileged access rights:** Restricción de acceso a base de datos. DuckDB Singleton aislará las credenciales y el acceso a los Parquet files.
*   **A.8.4 Access to source code:** Control de versiones estricto (Git) y ramas protegidas (develop/main).
*   **A.8.11 Data masking:** Enmascaramiento de datos (Hashing SHA-256) aplicado al instanciar Data Contracts.
*   **A.8.12 Data leakage prevention:** Medidas para evitar que los datos sensibles scrapeados salgan de los entornos locales o de la VPC autorizada.
*   **A.8.15 Logging:** Toda ejecución del orquestador, errores en extracción y fallas de validación de Pydantic deben registrarse (Logs) para poder ser analizados en caso de anomalías.
*   **A.8.16 Monitoring activities:** Monitorear comportamientos anómalos (ej. picos repentinos de extracción de datos).
*   **A.8.25 Secure development life cycle:** Reglas para un desarrollo seguro aplicadas durante todo el proyecto (Code Reviews, Linting con Ruff).
*   **A.8.27 Secure system architecture:** Aplicación de principios de ingeniería segura por diseño.
*   **A.8.28 Secure coding:** Aplicar los principios de Clean Code y evitar hardcodear credenciales o secretos en los scripts de Python.
*   **A.8.29 Security testing in development:** Implementar tests automatizados de seguridad (GitHub Actions) antes del paso a producción.
