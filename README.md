# 🌐 OmniVoC SaaS (Omnichannel Voice of Customer)

> *Nota: Inicialmente concebido como un "Indicador Sintético de Calidad de Banca Móvil", el alcance de este proyecto ha evolucionado a **OmniVoC SaaS**, una plataforma corporativa B2B de Inteligencia Artificial agnóstica a la industria.*
> **Significado:** **Omni**canal (extrae datos de todas las redes sociales y tiendas) + **V**oice **o**f **C**ustomer (Voz del Cliente).

¡Hola Boris y David! Bienvenidos al repositorio central de **OmniVoC**. Este documento es el manual principal para gestionar nuestro flujo de trabajo colaborativo usando Git y Antigravity. Dado que ambos estarán trabajando en paralelo, aquí definimos las bases para que nuestros entornos y agentes de IA estén perfectamente sincronizados.

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

**Al INICIAR tu sesión, copia y pégale esto a Antigravity:**
> *"Hola Antigravity, este es un proyecto colaborativo. Antes de hacer nada, asegúrate de hacer un `git pull origin develop` para traer los últimos cambios. Luego, lee el archivo `README.md`, los tableros en `docs/SCRUM/` y revisa la última entrada en `docs/AGENT_LOGS.md`. Explícame en qué estado se encuentra el proyecto y qué historia de usuario me toca abordar hoy según el Kanban."*

**Al FINALIZAR tu sesión, copia y pégale esto a Antigravity:**
> *"Hemos terminado por hoy. Por favor, escribe una nueva entrada detallada en `docs/AGENT_LOGS.md` indicando la fecha, quiénes somos, qué historia de usuario completamos, qué archivos modificamos y cuáles son los siguientes pasos sugeridos. Después de guardarlo, haz el commit y el push correspondiente a nuestra rama."*

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
