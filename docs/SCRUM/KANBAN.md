# Roadmap & Kanban Ágil (Meta: 11 de Junio de 2026)

Tenemos **5 días** para completar este proyecto integrador. Este es el roadmap comprimido por día. 
Antigravity debe mover las tareas a `[/]` cuando estén en progreso y a `[x]` cuando estén completadas.

## Sprint Acelerado (Jun 6 - Jun 11)

### [x] Día 1 (Junio 6): Estructuración y Reglas
- [x] Configurar repositorio y arquitectura (`docs/`).
- [x] Elaborar el mapeo de materias y reglas SOLID/Scrum.

### [ ] Día 2 (Junio 7): Datos (Ingeniería de Datos + Opt. Empresarial)
- [ ] Configurar el entorno Micromamba (R + Python).
- [ ] Desarrollar script PySpark para extraer reseñas de Apps bancarias (Play Store).
- [ ] Limpieza de datos en DuckDB y EDA (`ydata_profiling`).

### [ ] Día 3 (Junio 8): NLP (IA y ML I)
- [ ] Configurar MLflow.
- [ ] Desarrollar modelo NLP para clasificar sentimiento (positivo/negativo) y extraer fallas (bugs/caídas).
- [ ] Orquestar el flujo (Capa 4) de Extracción -> Limpieza -> Clasificación NLP.

### [ ] Día 4 (Junio 9): Econometría II y Optimización
- [ ] Construir Modelo Logit/Probit para predecir insatisfacción en base a fallas técnicas.
- [ ] Construir Cadenas de Markov estimando transición de usuarios Satisfechos -> Insatisfechos.
- [ ] Guardar resultados en BD (ACID).

### [ ] Día 5 (Junio 10): Dashboard (BI)
- [ ] Construir la interfaz en Streamlit.
- [ ] Integrar gráficas interactivas con Plotly.

### [ ] Día 6 (Junio 11): Cierre y Empaquetado
- [ ] Revisión de arquitectura (Principios SOLID).
- [ ] Validación de la norma ISO 9001 (Sistemas Integrados de Gestión).
- [ ] Congelar repositorio para presentación.
