# Proyecto: Indicador Sintético de Calidad de la Banca Móvil (Bolivia)

¡Hola Boris y David! Bienvenidos al repositorio central de nuestro proyecto final integrador. Este documento es el manual principal para gestionar nuestro flujo de trabajo colaborativo usando Git y Antigravity. Dado que ambos estarán trabajando en paralelo, aquí definimos las bases para que nuestros entornos y agentes de IA estén perfectamente sincronizados.

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

## 3. Estructura del Proyecto
*   `docs/`: El cerebro del proyecto. Aquí viven los apuntes de la universidad, el marco de trabajo Ágil (User Story Maps, Kanban) y los registros de los agentes.
*   `src/`: El código fuente, estructurado en una arquitectura profesional por capas.
*   `notebooks/`: Entornos de exploración y pruebas con datos (EDA, Databricks).

*Para detalles técnicos de la arquitectura, revisa el archivo `docs/HOW_WE_WORK.md`.*
