# Cumplimiento del Estándar ITIL 4 Foundation

Este documento condensa los conceptos clave, dimensiones, principios guía y prácticas de gestión de **ITIL 4** aplicables a la arquitectura de **OmniVoC SaaS**. Al ser una plataforma corporativa B2B, es vital adoptar un enfoque holístico de la gestión de servicios para entregar resultados continuos que generen valor tanto para nuestros clientes (bancos e instituciones) como para nosotros como proveedores.

## 1. El Sistema de Valor del Servicio (SVS)

En OmniVoC operamos bajo el SVS de ITIL 4, el cual describe cómo los componentes y actividades de la organización trabajan conjuntamente para facilitar la creación de valor. 

El núcleo del SVS es la **Cadena de Valor del Servicio**, que consta de seis actividades iterativas (Planear, Mejorar, Involucrar, Diseño y transición, Obtener/construir, Entregar y soportar). No operamos en cascada, sino que orquestamos estas actividades a través de nuestros pipelines CI/CD y automatizaciones.

## 2. Las 4 Dimensiones de la Gestión de Servicios

Ningún componente del servicio de analítica de datos se mantiene por sí solo. Evaluamos nuestras implementaciones usando cuatro dimensiones:

1. **Organizaciones y Personas:** Fomentamos una cultura colaborativa, previniendo el trabajo en silos ("silo activity"). Usamos Scrum, responsabilidades compartidas y fomentamos competencias multifuncionales (Data Engineers, Econometristas, MLOps, etc.).
2. **Información y Tecnología:** La infraestructura en la nube, bases de datos vectoriales, DuckDB en arquitectura Medallón y algoritmos de NLP son la columna vertebral tecnológica para extraer el conocimiento y asegurar su seguridad.
3. **Socios y Proveedores:** Las dependencias con terceros, como las APIs de tiendas de aplicaciones, el LLM utilizado o los servicios de alojamiento (ej. AWS, Ubicloud) deben contar con contratos claros y SLAs negociados.
4. **Procesos y Flujos de Valor:** Actividades optimizadas mediante automatización continua de código (GitHub Actions) y flujos iterativos definidos (Kanban).

## 3. Principios Guía de ITIL

Aplicamos los 7 principios guía en cada desarrollo y refactorización del proyecto:

1. **Sitúe el foco en el valor:** Todo código, modelo o proceso que desarrollemos debe crear valor (directo o indirecto) para nuestros clientes.
2. **Comience donde se encuentre:** Antes de reescribir un scraper entero, evaluamos qué código existente puede reutilizarse o repararse.
3. **Progrese de forma iterativa mediante la retroalimentación:** Desplegamos incrementos pequeños en lugar de un enfoque "Big Bang", evaluando métricas en cada ciclo.
4. **Colabore y promueva la visibilidad:** Usamos `AGENT_LOGS.md`, tableros Kanban, y una documentación estricta y pública en el repositorio.
5. **Piense y trabaje holísticamente:** No solo optimizamos la Base de Datos; pensamos en cómo ese cambio afecta al Dashboard (UI) y la extracción (Scraping).
6. **Manténgalo simple y práctico:** Reducimos la complejidad excesiva (ej. patrón Singleton para conexión a la DB) evitando consumir memoria y tiempo innecesario.
7. **Optimice y automatice:** Cualquier tarea repetitiva (linting, tests, construcción de infraestructura) se delega a las GitHub Actions, reservando la capacidad humana para decisiones de negocio y analítica.

## 4. Prácticas Clave de Gestión de Servicios

ITIL 4 propone un conjunto de prácticas, de las cuales hemos integrado rigurosamente las siguientes:

### A. Gestión de Incidentes
Su propósito es minimizar el impacto negativo mediante la rápida restauración de las operaciones (ej. caída de la base de datos o fallos del scraper debidos a un bloqueo de IP). Se establecerá un flujo rápido de resolución que incluya *swarming* para los fallos críticos del sistema.

### B. Gestión de Problemas y Error Conocido
Mientras la gestión de incidentes restaura el servicio, la gestión de problemas busca la causa raíz subyacente. Los errores estructurales (ej. fallas intermitentes del NLP) se registrarán como **Errores Conocidos** si todavía no pueden ser solucionados permanentemente y se documentarán mediante una **Solución Temporal (Workaround)** para reducir el impacto.

### C. Habilitación del Cambio
Para maximizar los despliegues exitosos y minimizar el riesgo. Gestionaremos:
- **Cambios Estándar:** Modificaciones simples de bajo riesgo preautorizadas (ej. reiniciar un worker, cambios cosméticos documentados en UI).
- **Cambios Normales:** Cambios importantes y de arquitectura (requerirán aprobación, documentados mediante *Architecture Decision Records*).
- **Cambios de Emergencia:** Parches críticos de seguridad o hotfixes (aplicados para mitigar un incidente grave).

### D. Mejora Continua
La mejora no es una actividad única sino el latido del SVS. Usaremos nuestro `AGENT_LOGS.md` y retrospectivas iterativas basadas en el modelo de mejora de ITIL (¿Cuál es la visión? ¿Dónde estamos ahora? ¿Cómo llegamos ahí? etc.) para registrar aprendizajes y optimizar el sistema.

### E. Mesa de Servicios (Service Desk)
El punto de entrada único de retroalimentación e interrupción de nuestros clientes. Integrado con un manejo de *solicitudes de servicio* y orquestado mediante soporte técnico de alto nivel si la resolución no puede manejarse en primera línea.
