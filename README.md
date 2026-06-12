# 🌐 OmniVoC SaaS (Omnichannel Voice of Customer)

> *Nota: Inicialmente concebido como un "Indicador Sintético de Calidad de Banca Móvil", el alcance de este proyecto ha evolucionado a **OmniVoC SaaS**, una plataforma corporativa B2B de Inteligencia Artificial agnóstica a la industria.*
> **Significado:** **Omni**canal (extrae datos de todas las redes sociales y tiendas) + **V**oice **o**f **C**ustomer (Voz del Cliente).

¡Hola David! Bienvenido al repositorio central de **OmniVoC**. Este documento es el manual principal para gestionar el flujo de trabajo usando Git y Antigravity.

## 1. El Flujo de Trabajo con Git (Gitflow)

Para evitar sobrescribir el código del otro accidentalmente o causar conflictos irresolubles, utilizaremos un modelo de ramas (branches). Piensa en las ramas como copias aisladas del proyecto donde puedes trabajar sin afectar la versión oficial.

### Estructura de Ramas
*   **`main`**: Es la rama de "Producción". Es sagrada. Solo debe contener código estable, completamente finalizado y aprobado por ambos. **Nunca programamos directamente aquí.**
*   **`develop`**: Es la rama de "Integración". Funciona como nuestra sala de ensamblaje. Cuando terminas una tarea, la traemos aquí para probarla junto con el trabajo del otro. **Tampoco programamos directamente aquí.**
*   **`feature/*`**: Son las ramas de "Trabajo Diario". Cada vez que vayas a programar algo nuevo, crearás una rama que nazca de `develop`. Por ejemplo: `feature/modelo-nlp` o `feature/extraccion-datos`.

### Tu Ciclo Diario de Trabajo (Paso a Paso)
1.  **Sincronización:** Al iniciar tu sesión, asegúrate de estar en tu computadora en la rama `develop` y descargar los últimos cambios que haya subido tu compañero:
    *   `git checkout develop`
    *   `git pull origin develop`
2.  **Nueva Tarea:** Crea tu rama de trabajo personal para la historia de usuario que elegiste:
    *   `git checkout -b feature/nombre-de-la-tarea`
3.  **Desarrollo:** Realiza los cambios necesarios.
4.  **Guardado Seguro:** Cuando termines por hoy, sube tus cambios a GitHub:
    *   `git add .`
    *   `git commit -m "Descripción breve de lo que hiciste"`
    *   `git push origin feature/nombre-de-la-tarea`
5.  **Integración:** Cuando la tarea esté totalmente lista y testeada, crearemos un *Pull Request* (PR) en GitHub para mover esos cambios desde tu rama `feature` hacia `develop`.

## 2. Cómo Sincronizar a los Agentes (Antigravity)

Los agentes de IA no tienen "telepatía" para saber qué hicimos en la computadora del otro. Nuestro repositorio es nuestro **"Segundo Cerebro"** (especialmente la carpeta `docs/`).

Para que los agentes tengan contexto instantáneo, SIEMPRE comunícate con ellos usando estas instrucciones al inicio y al final de tu día:

**Al INICIAR tu sesión (Para dar contexto al agente), copia y pega:**
> *"Hola Antigravity, inicia sesión. Haz un `git pull origin develop`. Luego, lee estrictamente TODO el contenido de `docs/ENGINEERING_STANDARDS/`, `docs/ADRs/`, `docs/GUIDES/` y `docs/BUSINESS_PRODUCT/` para entender las reglas del proyecto. Después, lee `docs/SCRUM/` y `docs/AGENT_LOGS.md`. Haz un paneo rápido por `src/`, `tests/` y `notebooks/`. Finalmente, dime qué historia de usuario nos toca hoy."*

**Al EJECUTAR una nueva tarea (Para forzar la calidad del código y crear la rama), copia y pega:**
> *"Vamos a trabajar en la Historia de Usuario [NÚMERO]. Primero, asegúrate de crear y cambiarte a una rama `feature/[nombre-tarea]` a partir de `develop`. Antes de programar nada, redacta un Implementation Plan justificando cómo cumplirás con `SOLID_PRINCIPLES.md`, `DEVOPS_MLOPS_SECURITY.md`, `DESIGN_PATTERNS.md` y `ISO_27002_COMPLIANCE.md`. Tras mi aprobación, a medida que escribas el código, asegúrate de ir realizando **Commits Atómicos** progresivos siguiendo `GIT_CHEATSHEET.md`."*

**Al FINALIZAR tu sesión (Para documentar, actualizar el progreso y guardar), copia y pega:**
> *"Hemos terminado por hoy. Primero, revisa `docs/SCRUM/USER_STORY_MAP.md` y `docs/SCRUM/KANBAN.md` para marcar con `[x]` las tareas y criterios de aceptación que completamos en esta sesión. Segundo, escribe una nueva entrada en `docs/AGENT_LOGS.md` indicando la fecha, autor, Vertical Slice, archivos modificados y cuál es la siguiente historia a trabajar. Tercero, verifica rápidamente que no hayamos roto ningún principio en `SOLID_PRINCIPLES.md`, `DEVOPS_MLOPS_SECURITY.md`, `DESIGN_PATTERNS.md` y `ISO_27002_COMPLIANCE.md`. Cuarto, verifica rápidamente si hay que actualizar, `DEFERRED_FEATURES.md`, `ARCHITECTURE_DECISIONS.md`, `GLOSSARY.md`, `SPECS_KIT.md`, `HOW_WE_WORK.md`, `MICROMAMBA_GUIDE.md` y `DATA_ARCHITECTURE.md`. Quinto, si se realizaron cambios en el paso anterior, escribe una nueva entrada en `docs/AGENT_LOGS.md`. Sexto, ejecuta **Commits Atómicos** siguiendo la convención de `GIT_CHEATSHEET.md` (feat, fix, docs, refactor). Séptimo, haz un `git push origin feature/[tu-rama]`, crea el Pull Request hacia `develop` con `gh pr create --base develop --fill`, y prográmalo para auto-merge con `gh pr merge --squash --auto`. Finalmente, muévete a la rama `develop`, haz `git pull origin develop` y elimina la rama local con `git branch -D feature/[tu-rama]`."*

## 3. Estructura de Directorios (Arquitectura del Proyecto)

Nuestro código está ordenado siguiendo los principios de Arquitectura por Capas, Patrones GoF y Clean Code.

```text
mobile_banking_indicator/
├── .gitignore             # Ignora entornos virtuales, datos pesados y caché
├── docs/                  # El Cerebro Corporativo y Gestión Scrum
│   ├── ADRs/                     # Ciclo de vida de Decisiones Arquitectónicas
│   │   └── ARCHITECTURE_DECISIONS.md
│   ├── BUSINESS_PRODUCT/         # Modelo de Negocio y Producto
│   │   ├── BUSINESS_MODEL.md
│   │   ├── DEFERRED_FEATURES.md
│   │   └── SPECS_KIT.md
│   ├── ENGINEERING_STANDARDS/    # Reglas de Código y Patrones
│   │   ├── DESIGN_PATTERNS.md
│   │   ├── DEVOPS_MLOPS_SECURITY.md # Políticas ISO 27001, CI/CD, Observabilidad y MLOps
│   │   ├── GLOSSARY.md
│   │   └── SOLID_PRINCIPLES.md
│   ├── GUIDES/                   # Guías Operativas
│   │   ├── GIT_CHEATSHEET.md
│   │   ├── HOW_WE_WORK.md
│   │   └── MICROMAMBA_GUIDE.md
│   ├── CONTEXT/                  # Material Teórico Universitario
│   │   ├── ai_collaboration_context.md
│   │   └── subjects_summary.md
│   └── SCRUM/                    # Tableros Kanban y User Story Maps
│       ├── KANBAN.md
│       └── USER_STORY_MAP.md
├── notebooks/             # Entornos de exploración y pruebas (Databricks / EDA)             # Tableros Kanban y User Story Maps
├── notebooks/             # Entornos de exploración y pruebas (Databricks / EDA)
├── tests/                 # Pruebas unitarias de las diferentes capas
└── src/                   # Código Fuente Principal
    ├── infrastructure/    # Conexiones: Scraping (Play Store), Base de Datos, APIs.
    ├── core/              # El Corazón: Entidades de negocio, Enums y Modelos de datos.
    ├── use_cases/         # Lógica pura: Algoritmos NLP, ETL con Spark, Econometría.
    ├── presentation/      # Interfaces: Código del Dashboard interactivo en Streamlit.
    └── orchestration/     # Capa 4: Menú interactivo CLI (construido con `rich`) que coordina todo.
```

## 4. Gestión del Conocimiento con NotebookLM (La Memoria del Proyecto)

Para asegurar que todo el contexto, las decisiones arquitectónicas complejas y las sesiones de código no se pierdan, mantenemos un flujo de exportación de conocimiento hacia **Google NotebookLM**.

Hemos creado la carpeta `docs/NOTEBOOKLM_LOGS/` que contiene los archivos maestros de consolidación:
*   `Antigravity_Logs_David.md`
*   `Antigravity_Logs_David.md`

**Al EXPORTAR una conversación (Para alimentar a NotebookLM), copia y pega este prompt:**
> *"He exportado el registro de nuestra última conversación en el archivo `[nombre_del_archivo_exportado.md]`. Por favor, toma TODO el contenido de ese archivo y añádelo al final de `docs/NOTEBOOKLM_LOGS/Antigravity_Logs_[David/David].md`. Utiliza ESTE formato exacto como separador antes de pegar el contenido, llenando los datos correspondientes:
>
> # ====================================================================================================
> # FECHA: [YYYY-MM-DD] | AUTOR: [Tu Nombre]
> # SESIÓN: [Número] | TEMA: [Tema principal de la conversación]
> # ====================================================================================================
>
> Una vez lo hayas añadido de forma segura, elimina el archivo temporal exportado original para mantener limpio el directorio de trabajo."*

1. **Exportar Conversaciones:** Usa el prompt de arriba siempre que descargues o agregues una sesión importante.
2. **Compilación Automática:** Antigravity se encargará de leer, formatear y concatenar el historial en el documento maestro correspondiente a tu usuario.
3. **Carga en NotebookLM:** Subiremos estos dos documentos consolidados a nuestro proyecto en NotebookLM de forma periódica.
4. **El Beneficio:** Esto convierte a NotebookLM en un "Oráculo" del proyecto que ha vivido todo el desarrollo paso a paso. Podremos usarlo para redactar la documentación final para la universidad, prepararnos para las defensas del proyecto, o simplemente preguntarle el porqué de una decisión técnica antigua, usando el historial real de trabajo como su fuente de verdad inmutable.
