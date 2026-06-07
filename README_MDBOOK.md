# Algoritmos y Estructuras de Datos - mdBook

📖 Página web interactiva de los apuntes de Algoritmos y Estructuras de Datos del Departamento de Ciencias de la Computación de la Universidad de Chile.

**🌐 Sitio web**: https://JR7juanito.github.io/AED

## 📚 Contenido

- **10 Capítulos** de teoría de algoritmos y estructuras de datos
- **7 Conjuntos** de ejercicios prácticos
- **Código Python** ejecutable con ejemplos
- **Análisis de complejidad** detallado

## 🚀 Inicio Rápido

### Compilar localmente

```bash
# 1. Instalar mdBook (si no lo tienes)
cargo install mdbook

# 2. Compilar el libro
mdbook build

# 3. Servir localmente (ver cambios en tiempo real)
mdbook serve
```

Abre http://localhost:3000 en tu navegador.

### Convertir Notebooks a Markdown

```bash
# Los notebooks .ipynb están en la raíz
# Ejecuta el script de conversión:
python convert_notebooks.py

# Esto actualizará automáticamente los archivos en src/
```

## 📁 Estructura

```
.
├── book.toml                  # Configuración de mdBook
├── src/                       # Contenido en Markdown
│   ├── README.md
│   ├── SUMMARY.md
│   ├── 01-introduccion.md
│   ├── ...
│   └── ejercicios/
├── recursos/                  # Imágenes y archivos
├── .github/workflows/         # CI/CD para GitHub Actions
│   └── deploy.yml
└── convert_notebooks.py       # Script de conversión
```

## 🔄 Flujo de trabajo

1. **Editar** los archivos `.md` en `src/`
2. **Probar localmente** con `mdbook serve`
3. **Hacer commit y push** a GitHub
4. **GitHub Actions** compila automáticamente
5. **GitHub Pages** publica el sitio

## ⚙️ Configuración

### GitHub Pages

1. Ve a **Settings → Pages**
2. Selecciona **Deploy from a branch**
3. Branch: `gh-pages` (se crea automáticamente)
4. Folder: `/ (root)`
5. ¡Guarda!

Tu sitio estará en: `https://JR7juanito.github.io/AED`

### Personalizar

Edita `book.toml` para cambiar:
- Título, autor, descripción
- Tema de colores
- Opciones de compilación

## 📖 Temas disponibles

1. Introducción
2. Métodos Matemáticos para el Análisis de Algoritmos
3. Diseño de Algoritmos Eficientes
4. Estructuras de Datos Elementales
5. Pilas, Colas y Colas de Prioridad
6. Diccionarios
7. Ordenación
8. Búsqueda en Texto
9. Compresión de Datos
10. Grafos

## 🛠️ Requisitos

- **Rust** y **Cargo**: https://rustup.rs/
- **mdBook**: `cargo install mdbook`
- **Python** (para convertir notebooks): `pip install nbconvert`

## 📝 Agregar contenido

### Crear nuevo capítulo

1. Crea `src/XX-nombre.md`
2. Agrega entrada en `src/SUMMARY.md`:
   ```markdown
   - [Título](./XX-nombre.md)
   ```
3. Compila y prueba

### Agregar ejercicios

1. Crea archivo en `src/ejercicios/`
2. Agrega a `src/SUMMARY.md` en sección de ejercicios

## 🎨 Temas disponibles

El sitio incluye temas claros y oscuros. Personaliza en `book.toml`:

```toml
[output.html]
default-theme = "light"
preferred-dark-theme = "navy"
```

## 🔗 Enlaces útiles

- [mdBook Documentation](https://rust-lang.github.io/mdBook/)
- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Pages Docs](https://pages.github.com/)

## 📄 Licencia

Este material es educativo y derivado del [repositorio oficial del DCC-UChile](https://github.com/ivansipiran/AED-Apuntes).

## 🤝 Créditos

- **Instructor**: Iván Sipirán
- **Universidad**: Universidad de Chile
- **Departamento**: Ciencias de la Computación
- **Basado en**: Apuntes anteriores de Patricio Poblete y Benjamín Bustos

---

**¿Necesitas ayuda?** Revisa [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
