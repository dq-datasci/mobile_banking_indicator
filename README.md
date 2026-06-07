# Proyecto: Indicador Sintético de Calidad de la Banca Móvil (Bolivia)

¡Hola Boris y David! Bienvenidos al repositorio de nuestro proyecto final integrador. Este documento es el manual principal para que tanto ustedes como sus agentes Antigravity sepan exactamente cómo operar aquí sin generar conflictos.

## 🌟 Para Boris: Cómo funciona esto y cómo no pisarnos los talones

Como estamos usando Inteligencia Artificial para acelerar el desarrollo (y tú estás en otra carrera que requiere conceptos distintos a los de software), hemos diseñado reglas a prueba de errores. Por favor sigue esto al pie de la letra:

### 1. El Flujo de Trabajo (Gitflow Simplificado)
Git nos permite trabajar en paralelo sin borrar lo que hace el otro.
*   **Nunca trabajes directamente en la rama `main` o `develop`.**
*   Cada vez que vayas a trabajar en algo (por ejemplo, el pipeline de datos), crea una "rama" nueva (branch). Tu agente Antigravity puede hacer esto por ti. Pídele: *"Crea una rama llamada feature/data-pipeline basada en develop"*.
*   **Antes de empezar el día**, dile a Antigravity: *"Actualiza el proyecto haciendo un git pull origin develop"*.
*   Cuando termines tu tarea, dile a Antigravity: *"Sube mis cambios y prepárate para integrarlos (Haz commit y push)"*.

### 2. Cómo comunicarte con Antigravity
Antigravity no "recuerda" por arte de magia lo que hizo mi agente en mi computadora. El "cerebro compartido" vive en la carpeta `docs/`.
**Cada vez que inicies sesión, dale esta instrucción exacta a Antigravity:**
> *"Hola, antes de hacer nada, haz `git pull origin develop`. Luego lee el archivo `README.md`, el archivo `docs/SCRUM/KANBAN.md`, los contextos en `docs/CONTEXT/` y el archivo `docs/AGENT_LOGS.md` para que sepas en qué nos quedamos."*

**Cada vez que termines tu sesión, dale esta instrucción:**
> *"Registra todo lo que logramos hoy en el archivo `docs/AGENT_LOGS.md` explicando claramente en qué nos quedamos para que el otro agente lo sepa. Luego haz commit y push."*

## 📚 Estructura del Proyecto

*   `docs/`: El cerebro del proyecto. Aquí viven los apuntes de NotebookLM, el Kanban (Scrum) y las decisiones de arquitectura.
*   `src/`: El código fuente.
*   `notebooks/`: Para exploración de datos en Databricks.

¡Cualquier duda técnica está explicada a detalle para los agentes en `docs/HOW_WE_WORK.md`!
