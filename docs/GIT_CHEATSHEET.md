# Guía de Supervivencia: Git para este Proyecto

Git es un sistema que guarda el historial de nuestro código. Piensa en Git como una máquina del tiempo combinada con universos paralelos (ramas o *branches*). Aquí están los comandos esenciales que tú y Boris usarán día a día.

## 1. Ver cómo estamos (El Mapa)

*   `git status`
    **¿Qué hace?** Te dice en qué rama estás parado y qué archivos has modificado pero aún no has guardado. **Úsalo todo el tiempo** si te sientes perdido.
*   `git branch`
    **¿Qué hace?** Lista todos los "universos paralelos" locales. El que tiene un asterisco (`*`) verde es en el que estás ahora mismo.

## 2. Iniciar el Día (Traer cambios del otro)

*   `git checkout develop`
    **¿Qué hace?** Te mueve a la rama de integración principal (develop).
*   `git pull origin develop`
    **¿Qué hace?** Descarga de GitHub todo lo que tu compañero programó anoche y lo junta con lo que tienes en tu computadora. **¡Regla de oro: haz esto antes de empezar a programar!**

## 3. Crear una Nueva Tarea (Crear tu Universo)

*   `git checkout -b feature/nombre-de-tarea`
    *(Ejemplo: `git checkout -b feature/limpieza-datos`)*
    **¿Qué hace?** Crea una rama nueva idéntica a `develop` y te mueve a ella automáticamente. Aquí es donde debes programar. Tu compañero no verá lo que haces aquí hasta que lo subas.

## 4. Guardar tu Progreso (La Foto del Momento)

*   `git add .`
    **¿Qué hace?** Prepara *todos* los archivos que modificaste para ser guardados. (El punto `.` significa "todo en esta carpeta").
*   `git commit -m "Aquí explicas qué hiciste"`
    *(Ejemplo: `git commit -m "Limpiar emojis de las reseñas de la Play Store"`)*
    **¿Qué hace?** Toma la "foto" oficial de tus archivos y la guarda en tu computadora con el mensaje que escribiste.

## 5. Subir a GitHub (Compartir con tu compañero)

*   `git push origin feature/nombre-de-tarea`
    **¿Qué hace?** Envía la "foto" que tomaste (commit) a los servidores de GitHub. A partir de este momento, tu compañero puede ver tu código en internet.

## 💡 Resumen del Flujo Diario
1. `git checkout develop` -> `git pull origin develop` (Actualizas tu compu).
2. `git checkout -b feature/mi-tarea` (Creas tu rama).
3. *...escribes código...*
4. `git add .` -> `git commit -m "Terminé mi tarea"` (Guardas).
5. `git push origin feature/mi-tarea` (Subes a internet).
