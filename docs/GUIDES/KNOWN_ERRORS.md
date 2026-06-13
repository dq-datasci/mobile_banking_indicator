# Errores Conocidos y Habilitación del Cambio (Known Errors)

En cumplimiento de la **Historia 1.5.4**, este documento funciona como el registro centralizado de problemas recurrentes (Problem Management) para el ecosistema OmniVoC. Siguiendo las directrices de ITIL 4, aquí se documentan las **Soluciones Temporales (Workarounds)** mientras se desarrolla una solución estructural mediante la **Habilitación del Cambio**.

## 1. Política de Habilitación del Cambio en CI/CD

Todo cambio que busque resolver un error estructural debe pasar por el flujo de "Cambio Normal" a través de GitHub Actions:
1. **Creación de Rama:** `feature/nombre-resolucion`.
2. **Pruebas Automatizadas:** El código debe superar las validaciones de `pytest` y `ruff` (Shift-left testing).
3. **Revisión por Pares:** Se requiere al menos un *approval* en el Pull Request antes de fusionar a `develop`.
4. **Cierre de Error:** Una vez desplegado, el error correspondiente en este documento se marcará como `[RESUELTO]`.

---

## 2. Registro de Errores Conocidos (KEDB - Known Error Database)

A continuación, se listan los problemas detectados que aún no tienen solución permanente.

### KE-001: Rate Limiting severo en App Store Scraper
* **Fecha de Registro:** 2026-06-12
* **Descripción:** La API no oficial de Apple App Store bloquea la IP del worker si se solicitan más de 5 páginas de reseñas de forma concurrente.
* **Impacto:** Falla la ingesta total del día en la capa Bronze. (Severidad: Alta).
* **Workaround (Solución Temporal):** El `ScraperFactory` incluye un retraso forzado (`time.sleep(2)`) y reintento con backoff exponencial. Se recomienda no ejecutar el pipeline completo más de 2 veces por hora.
* **Solución Permanente Planeada:** Implementar rotación de Proxies o IP dinámicas en el scraper (Asignado al Sprint 4).

### KE-002: Inconsistencias de Tipo en DuckDB con Pydantic
* **Fecha de Registro:** 2026-06-12
* **Descripción:** Pydantic a veces castea enteros largos como strings, causando que la capa Silver falle al insertar en DuckDB con un error de Type Mismatch.
* **Impacto:** Los datos no pasan a la capa Silver, paralizando el dashboard. (Severidad: Media).
* **Workaround (Solución Temporal):** Uso del método `.astype()` de pandas justo antes de llamar a `conn.execute()` en la base de datos Singleton.
* **Solución Permanente Planeada:** Definir `Strict=True` en todos los modelos Pydantic del `review_contract.py` para forzar validación estricta desde la instanciación.

### KE-003: Out Of Memory (OOM) en ydata-profiling con Big Data
* **Fecha de Registro:** 2026-06-13
* **Descripción:** La librería `ydata-profiling` usa Pandas en memoria. Al inyectar la carga masiva de reseñas reales, el proceso colapsa por falta de RAM al intentar calcular matrices de correlación e interacciones exhaustivas.
* **Impacto:** El pipeline se cae y falla la generación del Análisis Exploratorio de Datos (EDA). (Severidad: Crítica).
* **Workaround (Solución Temporal):** Reemplazar el motor del EDA Global por PySpark (cálculos estadísticos distribuidos *out-of-core*) y usar `ydata-profiling` únicamente sobre una muestra (sample) reducida del banco cliente objetivo (ej. BCP).
* **Solución Permanente Planeada:** Mantener PySpark para todo análisis exploratorio sobre capas Silver/Gold e implementar Data Observability nativo en el Lakehouse.
