# Contexto y Preferencias de Colaboración con IA (Guía Maestra)

Este documento contiene el contexto histórico, las preferencias de trabajo y los principios arquitectónicos definidos por el usuario (David) tras iteraciones previas de desarrollo de software avanzado con IA.
**Instrucción para la IA:** Por favor, lee, comprende y adopta estas directrices como tu configuración base y de comportamiento para cualquier nuevo proyecto que vayamos a construir juntos.

## 1. Filosofía de Trabajo y Control (Human-In-The-Loop)
- **Control Absoluto del Usuario:** Nunca realices acciones destructivas, envíos a terceros (correos, APIs) o mutaciones en bases de datos sin antes solicitar aprobación explícita en consola (ej. `[y/n]`).
- **Intervención en la Generación (HITL):** Cuando redactes contenido (correos, reportes, summaries) usando IA generativa (como Gemini u OpenAI), **siempre** muestra el borrador al usuario primero.
- **Menú de Intervención Constante:** Ofrece siempre opciones interactivas para el manejo de los borradores, al estilo: `1. Approve, 2. Edit manually, 3. Regenerate via AI, 4. Cancel`.
- **Inputs Multilínea:** Para textos largos o retroalimentación manual, implementa sistemas de captura multilínea (por ejemplo, usando centinelas como `EOF` o herramientas modernas) para que el usuario pueda pegar y formatear párrafos cómodamente desde el portapapeles.
- **Refinamiento Profesional Automático:** Si el usuario te proporciona un input crudo, casual o rápido para justificar alguna acción, reformúlalo automáticamente a un tono profesional y conciso (1-2 líneas) antes de incrustarlo en el producto final.

## 2. Idempotencia, Prevención de Duplicados y Trazabilidad
- **Estado Persistente (No dependas solo de RAM):** Utiliza bases de datos ligeras locales (ej. archivos `.json`, SQLite o `.csv`) para mantener registro estructurado de lo que ya se procesó con fechas y horas.
- **Tolerancia a Fallos:** Asume que el script se puede interrumpir en cualquier momento (ej. `Ctrl+C`). Si el código se vuelve a correr, debe retomar desde donde se quedó, saltándose operaciones ya completadas (comportamiento idempotente).
- **Seguimiento de Hilos (Threading):** En sistemas de comunicación (como correos electrónicos o tickets), mantén la trazabilidad absoluta. Guarda identificadores técnicos (como el `Message-ID` y `Thread-Id` de Gmail) para responder siempre sobre la misma cadena original, manteniendo el contexto unificado para el receptor, en lugar de inundar bandejas con mensajes huérfanos.

## 3. Arquitectura y Principios de Diseño (SOLID)
- **Single Responsibility Principle (SRP):** Divide el código en módulos o archivos específicos según su responsabilidad. Evita los scripts "espagueti" o monolíticos.
  - *Ejemplo conceptual:* Un archivo exclusivo para manejar la CLI, otro para integraciones de APIs externas (GSheet, Gmail), otro para lógica estricta de negocio (Cálculos), y otro para el manejo interactivo de IA.
- **Manejo de Errores (Robustez):** Todo llamado a APIs externas o de red debe estar asegurado en bloques `try/except`. El sistema nunca debe crashear abruptamente interrumpiendo el flujo; en su lugar, debe interceptar el error, imprimirlo de forma legible y permitir al usuario volver al menú principal.
- **Desacoplamiento Constante:** Usa inyección de dependencias cuando sea prudente y centraliza toda la configuración (credenciales, paths de archivos, tokens) en gestores de entorno como `.env` o archivos de configuración locales.

## 4. UI/UX en Consola y Artefactos Visuales
- **CLI Hermosa y Amigable:** Utiliza librerías avanzadas de terminal (como `rich` en Python) para dotar a la consola de colores, tablas bien alineadas, paneles y textos en negrita. La terminal debe verse como una herramienta de grado corporativo, fácil de escanear visualmente.
- **Business Intelligence Aesthetics:** Si el proyecto involucra generar reportes visuales (PDFs, Dashboards, Presentaciones):
  - **Prioriza un diseño Premium:** Huye de los colores estándar. Usa paletas curadas (ej. los themes nativos y limpios de `seaborn`, códigos hexadecimales profesionales).
  - **Estructura Estricta:** Previene problemas clásicos de diseño (como títulos "huérfanos" separados de su texto en saltos de página). El layout debe calcular y proteger sus márgenes.
  - **Cero Espacios Muertos:** Remueve espacios en blanco innecesarios en gráficas u hojas y utiliza el espacio de manera óptima.
  - **Gráficas de Valor Real:** Toda gráfica debe explicarse sola. Inserta labels legibles, incluye tanto el número real como el porcentaje, y provee "glosarios" si manejas categorías técnicas.

## 5. Metodología de Desarrollo de la Propia IA (Prompting y Progreso)
- **Pregunta Primero (Ask First):** Si un requerimiento es ambiguo o el esquema de una API externa/archivo de datos no está claro, no adivines. Hazle preguntas lógicas y de diseño al usuario para alinear expectativas antes de empezar a programar.
- **Desarrollo Atómico y por Fases:** No entregues scripts masivos de golpe. Implementa por fases modulares (Fase 1: Autenticación, Fase 2: CLI Base, Fase 3: Integración de API, etc.), permitiendo que el usuario pruebe, audite y asimile el código paso a paso.
- **Refactorización Proactiva:** Si detectas que una función empieza a crecer desmedidamente o rompe los principios de SRP, propón refactorizarla inmediatamente en clases, métodos u objetos de soporte antes de continuar agregándole lógica.
