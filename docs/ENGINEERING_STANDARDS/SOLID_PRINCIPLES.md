# Principios SOLID Aplicados

Para garantizar que nuestro Monolito Modular mantenga la limpieza y escalabilidad de un entorno de microservicios, el código se regirá estrictamente por los 5 principios SOLID.

## 1. Single Responsibility Principle (SRP)
**Definición:** Una clase o módulo debe tener una, y solo una, razón para cambiar.
**Implementación en el Proyecto:**
*   Los scrapers (ej. `PlayStoreScraper`) *solo* extraen datos. No los limpian ni calculan sentimientos.
*   El Dashboard (Streamlit) *solo* dibuja píxeles en la pantalla. No hace consultas directas SQL ni entrena modelos ML.

## 2. Open/Closed Principle (OCP)
**Definición:** El software debe estar abierto para extensión, pero cerrado para modificación.
**Implementación en el Proyecto:**
*   Si mañana el Banco nos pide extraer quejas desde correos electrónicos corporativos, NO modificaremos el archivo principal de extracción. Crearemos un nuevo `EmailScraper` que herede de la misma interfaz y lo inyectaremos en el pipeline, respetando el código existente.

## 3. Liskov Substitution Principle (LSP)
**Definición:** Las clases derivadas deben poder sustituir a sus clases base sin romper el programa.
**Implementación en el Proyecto:**
*   Todas nuestras clases de extracción heredarán de una clase base abstracta `BaseScraper`. Así, el orquestador principal podrá llamar al método `extract_reviews()` sin importar si está hablando con Twitter, Reddit o la App Store, garantizando polimorfismo seguro.

## 4. Interface Segregation Principle (ISP)
**Definición:** Es mejor tener muchas interfaces pequeñas y específicas que una sola interfaz enorme de propósito general.
**Implementación en el Proyecto:**
*   No obligaremos a que nuestro `NLPModel` implemente métodos de "Limpieza de StopWords" y "Traducción" si solo lo usamos para Sentimiento. Dividiremos las herramientas del Data Scientist en clases modulares pequeñas.

## 5. Dependency Inversion Principle (DIP)
**Definición:** Los módulos de alto nivel no deben depender de los de bajo nivel. Ambos deben depender de abstracciones.
**Implementación en el Proyecto:**
*   La lógica de negocio (capa `src/use_cases`) no importará la librería `google_play_scraper` directamente. Dependerá de una *Interface/Protocol* de Python. Esto significa que si mañana cambian la API de la Play Store y se rompe la librería, la lógica central del negocio se mantendrá intacta.
