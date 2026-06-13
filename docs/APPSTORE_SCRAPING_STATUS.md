# Estado del Scraping de la App Store

A partir del Sprint 1 (Extracción de Datos), se ha tomado la decisión de **suspender temporalmente la recolección de comentarios desde la Apple App Store** y eliminar los datos parciales extraídos.

## Motivos de la Suspensión

1. **Depreciación de la API Pública de Apple:** 
   El feed RSS tradicional de iTunes que se utilizaba para extraer reseñas (`https://itunes.apple.com/.../rss/customerreviews/.../json`) ha sido deshabilitado por Apple y ahora devuelve 0 resultados globalmente para cualquier aplicación.

2. **Bloqueo a Librerías Tradicionales:**
   La librería estándar de Python (`app_store_scraper`) está rota porque dependía de un token JWT estático (`web-experience-app/config/environment`) que Apple eliminó del código fuente HTML de su página web.

3. **Restricciones Severas (HTTP 429):**
   Cualquier intento de consumir la API interna moderna de Apple (`https://apps.apple.com/api/apps/v1/catalog/...`) mediante HTTP requests tradicionales falla con un error `429 Too Many Requests` debido a la validación estricta de cookies, headers y "browser fingerprinting" (huella digital del navegador).

4. **Fragmentación Regional de Comentarios:**
   Apple aísla los comentarios de forma estricta por país. Una aplicación boliviana con 300 reseñas globales puede mostrar únicamente 6 o 10 comentarios si se consulta específicamente la tienda de Bolivia (`country=bo`).

## Solución Descartada
Se logró desarrollar una prueba de concepto exitosa utilizando **Playwright** (un navegador headless) para interceptar el tráfico de red de la API interna de Apple y simular "scrolls" en múltiples países. Sin embargo, se decidió no implementar esta solución para:
- Evitar ensuciar el entorno con dependencias pesadas (Node.js, navegadores de Playwright, etc.).
- Mantener la arquitectura de extracción de datos simple y confiable.

## Próximos Pasos
Por el momento, el análisis y los pipelines de procesamiento posteriores (Silver/Gold) se realizarán **exclusivamente con los datos de la Google Play Store**, los cuales son abundantes y se pueden extraer de manera estable.
