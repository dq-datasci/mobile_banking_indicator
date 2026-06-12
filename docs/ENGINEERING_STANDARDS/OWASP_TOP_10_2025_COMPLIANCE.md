# Cumplimiento del Estándar OWASP Top 10 (2025)

Este documento destila los riesgos críticos de seguridad en aplicaciones web identificados por la **OWASP Top 10 2025**, proporcionando el contexto de cómo deben ser mitigados dentro del ciclo de vida de desarrollo seguro de nuestro producto B2B (OmniVoC SaaS).

## Riesgos y Estrategias de Prevención

### A01:2025 - Broken Access Control
Fallos donde los usuarios actúan fuera de sus permisos previstos, como evasiones de controles de acceso o elevación de privilegios.
**Prevención en el Proyecto:**
- Implementar **Deny by default** (Denegar por defecto).
- Modelar controles de acceso centralizados (ej. dependencias en FastAPI) e implementarlos una sola vez, reutilizándolos en los endpoints.
- Aplicar Rate Limiting a las APIs para minimizar daños.
- Desactivar el listado de directorios en el servidor web.

### A02:2025 - Security Misconfiguration
Falta de fortificación de la seguridad, configuraciones por defecto inseguras o mensajes de error que exponen "stack traces".
**Prevención en el Proyecto:**
- Mantener un proceso de *hardening* (fortificación) automatizado e "Infrastructure as Code" (IaC) para entornos consistentes.
- Segmentar la arquitectura (ej. base de datos DuckDB aislada en subred privada, sin exposición pública).
- Enviar directivas de seguridad en cabeceras HTTP.
- Remover funcionalidades, frameworks o documentación que no se utilicen.

### A03:2025 - Software Supply Chain Failures
Uso de componentes de software (librerías, dependencias) obsoletos, vulnerables o no mantenidos.
**Prevención en el Proyecto:**
- Escanear continuamente las dependencias y hacer inventarios. Se integrarán herramientas en el CI/CD (ej. `safety` o el sistema nativo de GitHub Dependabot).
- Eliminar dependencias innecesarias (cumpliendo con Single Responsibility Principle y uso de Micromamba).

### A04:2025 - Cryptographic Failures
Transmisión o almacenamiento de datos sensibles en texto claro, o uso de algoritmos criptográficos débiles.
**Prevención en el Proyecto:**
- Encriptar todos los datos sensibles (Privacy by Design - Hashing SHA-256 ya implementado para PII).
- Desactivar la caché para respuestas que contengan datos sensibles.
- Usar funciones de hash adaptables fuertes (Argon2, bcrypt) para contraseñas.
- Descontinuar el uso de protocolos y hashes deprecados (MD5, SHA1).

### A05:2025 - Injection
Falta de validación o filtrado en entradas proporcionadas por el usuario que resultan en inyección de código SQL, NoSQL, o Comandos.
**Prevención en el Proyecto:**
- Utilizar exclusivamente consultas parametrizadas o librerías ORM robustas.
- Pydantic Data Contracts serán la primera barrera: validar, filtrar y sanitizar rigurosamente cada input externo antes de interactuar con el Lakehouse o la API.

### A06:2025 - Insecure Design
Errores en el diseño o arquitectura donde los controles de seguridad no fueron modelados para combatir riesgos de negocio.
**Prevención en el Proyecto:**
- Integrar la seguridad en las User Stories (DevSecOps).
- Aplicar *Threat Modeling* para autenticación, control de acceso y flujos clave.
- Validar mediante *Unit* e *Integration Tests* los flujos críticos.
- Asegurar la segregación entre capas lógicas del Monolito Modular.

### A07:2025 - Authentication Failures
Ataques como relleno de credenciales (credential stuffing), ataques de fuerza bruta, o exposición de Session IDs en URLs.
**Prevención en el Proyecto:**
- Implementar Autenticación Multi-Factor (MFA) si es aplicable.
- Alinear políticas de contraseñas y rotación con NIST 800-63b.
- Evitar credenciales por defecto (`admin/admin`).
- Limitar y retrasar progresivamente intentos fallidos de inicio de sesión.
- Utilizar manejadores de sesión seguros que generen IDs aleatorios de alta entropía y no exponerlos nunca en URLs.

### A08:2025 - Integrity Failures
Ocurren cuando la aplicación confía en repositorios, plugins, CI/CD o CDNs sin verificar firmas ni repositorios de confianza, resultando en inyección de código malicioso.
**Prevención en el Proyecto:**
- Utilizar firmas digitales para verificar software.
- Validar el origen de las librerías utilizando repositorios oficiales y herramientas de seguridad para cadena de suministro en el pipeline CI/CD.
- Requerir de Pull Requests obligatorios y Code Reviews estrictos.

### A09:2025 - Logging & Alerting Failures
No registrar errores de seguridad ni ser capaces de emitir alertas o responder ante ataques activos.
**Prevención en el Proyecto:**
- Todo evento de seguridad importante debe utilizar el `AuditLogger` centralizado.
- Monitorear logs de manera central y segura.
- Configurar alertas de escalación, permitiendo detección en tiempo real.

### A10:2025 - Mishandling of Exceptions
Ocurre cuando el software no previene, detecta ni se recupera adecuadamente de excepciones no controladas, derivando en caídas, fugas de lógica o exposición de datos.
**Prevención en el Proyecto:**
- Manejo centralizado de excepciones (ej. Middlewares de FastAPI).
- Implementar `try/except` rigurosos (Failing Safely) sin filtrar stack traces al cliente.
- Testear agresivamente los escenarios de fallo (Chaos Engineering / Resiliencia).
