# Patrones y Antipatrones de Diseño - Material Educativo

Este repositorio contiene material educativo para la enseñanza de patrones y antipatrones de diseño en programación, específicamente diseñado para estudiantes de Ingeniería de Sistemas de 6º y 7º semestre.

## 📚 Contenido

### 1. Ejemplo Demostrativo
- **`demo_antipatterns_example.py`**: Archivo con ejemplos claros de antipatrones comunes para demostración en clase
  - God Object (Objeto Dios)
  - Spaghetti Code (Código Espagueti)
  - Copy-Paste Programming (Programación Copiar-Pegar)

### 2. Ejercicios Prácticos
Serie de archivos con código problemático para que los estudiantes identifiquen antipatrones:
- **`exercise_inventory_system.py`**: Sistema de gestión de inventario
- **`exercise_banking_api.py`**: API de servicios bancarios
- **`exercise_course_platform.py`**: Plataforma de cursos online

### 3. Instrucciones
- **`EXERCISE_INSTRUCTIONS.md`**: Guía detallada para los estudiantes sobre cómo realizar el ejercicio

## 🎯 Objetivo

El objetivo de este material es ayudar a los estudiantes a:
- Identificar antipatrones comunes en código real
- Comprender por qué estos patrones son problemáticos
- Desarrollar habilidades de análisis crítico del código
- Proponer soluciones y refactorizaciones apropiadas

## 🕐 Duración

- **Demostración**: 15-20 minutos
- **Ejercicio práctico**: 30 minutos
- **Discusión de resultados**: 15-20 minutos

## 📝 Antipatrones Incluidos

1. **God Object/God Class**: Clases que tienen demasiadas responsabilidades
2. **Spaghetti Code**: Código con lógica enredada y difícil de seguir
3. **Copy-Paste Programming**: Duplicación excesiva de código
4. **Long Method**: Métodos extremadamente largos
5. **Global State**: Uso excesivo de variables globales
6. **Magic Numbers/Strings**: Valores hardcodeados sin contexto
7. **Feature Envy**: Clases que usan excesivamente datos de otras clases
8. **Singleton Abuse**: Mal uso del patrón Singleton

## 🚀 Cómo usar este material

### Para el instructor:
1. Comenzar con `demo_antipatterns_example.py` para explicar cada antipatrón
2. Mostrar cómo identificar los problemas y sus consecuencias
3. Distribuir los ejercicios a los estudiantes

### Para los estudiantes:
1. Leer las instrucciones en `EXERCISE_INSTRUCTIONS.md`
2. Analizar los archivos de ejercicio
3. Documentar los antipatrones encontrados siguiendo el formato sugerido
4. Proponer soluciones de refactorización

## 💡 Tips para la identificación

- Buscar clases con más de 10 atributos o métodos
- Identificar métodos con más de 50 líneas
- Encontrar código repetido más de 2 veces
- Detectar anidación excesiva de condicionales
- Revisar el uso de variables globales

## 📖 Recursos adicionales recomendados

- "Clean Code" por Robert C. Martin
- "Refactoring: Improving the Design of Existing Code" por Martin Fowler
- Principios SOLID
- Catálogo de patrones de diseño GoF (Gang of Four)

---

**Nota**: Este código contiene antipatrones intencionales con fines educativos. NO utilizar estas prácticas en código de producción.