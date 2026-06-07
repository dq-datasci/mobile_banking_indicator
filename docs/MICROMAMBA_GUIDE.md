# Guía de Micromamba: Nuestro Entorno de Trabajo

Para que el código de David funcione exactamente igual en la computadora de Boris, necesitamos un entorno virtual. Un entorno virtual es como una "burbuja" donde instalamos versiones específicas de Python, R y librerías sin alterar el resto de la computadora.

Nosotros usamos **Micromamba** (una versión ultrarrápida de Conda) porque permite instalar tanto Python (para Machine Learning) como R (para Econometría) en la misma burbuja.

## 1. Crear la Burbuja (Solo se hace una vez)

Abre la terminal en la carpeta del proyecto y ejecuta:
```bash
micromamba create -n banco_env python=3.10 r-base
```
**¿Qué hace?** Crea un entorno virtual llamado `banco_env` con Python versión 3.10 y el lenguaje R preinstalados. Micromamba te preguntará si estás de acuerdo, presiona `Y` (Yes) y luego Enter.

## 2. Entrar a la Burbuja (Cada vez que vayas a trabajar)

```bash
micromamba activate banco_env
```
**¿Qué hace?** Te "mete" dentro de la burbuja. Notarás que el texto de tu terminal cambia para mostrar `(banco_env)` al principio. **Siempre debes hacer esto antes de ejecutar cualquier código.**

*(Nota: Para salir de la burbuja y volver a la normalidad de tu computadora, usa `micromamba deactivate`).*

## 3. Instalar Paquetes (Librerías)

Si necesitas instalar algo nuevo para analizar datos, hazlo así (asegúrate de que el entorno esté activado):

**Para librerías de Python (Pip es el estándar):**
```bash
pip install pandas numpy streamlit plotly
```

**Para instalar Quarto (reportes) y herramientas complejas (Databricks/Spark):**
```bash
micromamba install -c conda-forge pyspark mlflow quarto
```

## 4. Compartir el Entorno (Exportar)

Si Boris necesita instalar exactamente las mismas librerías que David descubrió y usó ayer, David debe exportar la lista y Boris debe leerla.

**Paso 1 (David):** Exporta las librerías a un archivo:
```bash
micromamba env export > environment.yml
```
*(Luego, David debe hacer un commit de ese archivo `environment.yml` a Git y subirlo).*

**Paso 2 (Boris):** Después de hacer `git pull` y ver que hay un `environment.yml` nuevo, Boris actualiza su burbuja así:
```bash
micromamba update -n banco_env -f environment.yml
```

## 💡 Flujo de Trabajo con Micromamba
1. Abres la terminal en la carpeta del proyecto.
2. Escribes `micromamba activate banco_env`.
3. ¡Empiezas a programar y correr scripts!
