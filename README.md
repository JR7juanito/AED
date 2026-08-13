# Algoritmos y Estructuras de Datos - mdBook

📖 **Sitio web**: https://JR7juanito.github.io/AED

Este es el repositorio con la página web interactiva del curso "Algoritmos y Estructuras de Datos" del [Departamento de Ciencias de la Computación](http://www.dcc.uchile.cl) de la [Universidad de Chile](http://www.uchile.cl). 

El contenido está basado en el [repositorio oficial de Iván Sipirán](https://github.com/ivansipiran/AED-Apuntes) y ha sido convertido a **mdBook** para publicación en GitHub Pages.

## Utilidades para JupyterLite + Pyodide

Se agregó un módulo local `aed_utilities/` para usar en entornos web sin instalación por `pip`.

```python
import aed_utilities as aed
```

Incluye versiones compatibles de `LinkedListDrawer`, `BinaryTreeDrawer`, `Tree23Drawer`, `GraphDrawer`, `NumpyArrayDrawer` y los `demo_*`.

### Probar en JupyterLite público (REPL)

Sí, lo puedes testear aquí: https://jupyterlite.github.io/demo/repl/index.html

En una celda Python:

```python
import micropip
await micropip.install("https://raw.githubusercontent.com/JR7juanito/AED/37a7e8a/dist/aed_utilities_web-0.1.0-py3-none-any.whl")
import aed_utilities as aed
```

Si eso corre sin error, quedó **público e importable**.

Validación rápida:

```python
aed.__version__
```

**Contenido**: Apuntes en Python en formato Jupyter Notebook, convertidos a Markdown para lectura web interactiva.

## Temario del Curso

### 📚 Temas principales
  1. [Introducción](https://jr7juanito.github.io/AED/01-introduccion.html)
  2. [Métodos matemáticos para el análisis de algoritmos](https://jr7juanito.github.io/AED/02-metodos-matematicos.html)
  3. [Diseño de algoritmos eficientes](https://jr7juanito.github.io/AED/03-diseño-algoritmos.html)
  4. [Estructuras de datos elementales](https://jr7juanito.github.io/AED/04-estructuras-datos.html)
  5. [Pilas, colas y colas de prioridad](https://jr7juanito.github.io/AED/05-pilas-colas.html)
  6. [Diccionarios](https://jr7juanito.github.io/AED/06-diccionarios.html)
  7. [Ordenación](https://jr7juanito.github.io/AED/07-ordenacion.html)
  8. [Búsqueda en texto](https://jr7juanito.github.io/AED/08-busqueda-texto.html)
  9. [Compresión de datos](https://jr7juanito.github.io/AED/09-compresion-datos.html)
  10. [Grafos](https://jr7juanito.github.io/AED/10-grafos.html)

### 🏋️ Ejercicios prácticos
- [Ejercicios de cada tema disponibles en la web](https://jr7juanito.github.io/AED/)

## 🚀 Acceso rápido

**📖 Leer en línea**: https://jr7juanito.github.io/AED

**💻 Desarrollo local**:
```bash
mdbook serve
```

**🔧 Convertir notebooks**:
```bash
python convert_notebooks.py
```
