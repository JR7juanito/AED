# Guía de Compilación y Despliegue

## 📋 Prerequisitos

Necesitas tener instalado:
- **Rust** y **Cargo**: https://rustup.rs/
- **mdBook**: Se instala con `cargo install mdbook`

## 🛠️ Compilar localmente

```bash
# Instalar mdBook (si no está instalado)
cargo install mdbook

# Compilar el libro
mdbook build

# Ver en navegador (servidor local)
mdbook serve
```

Luego abre http://localhost:3000 en tu navegador.

## 📝 Estructura del proyecto

```
.
├── book.toml              # Configuración de mdBook
├── src/
│   ├── README.md          # Portada
│   ├── SUMMARY.md         # Índice
│   ├── 01-introduccion.md
│   ├── 02-metodos-matematicos.md
│   ├── ...
│   └── ejercicios/        # Ejercicios por tema
├── .github/
│   └── workflows/
│       └── deploy.yml     # Workflow para GitHub Actions
└── recursos/              # Imágenes y archivos auxiliares
```

## 🚀 Despliegue en GitHub Pages

El despliegue es **automático**:

1. Cualquier push a `main` o `master` dispara el workflow
2. GitHub Actions compila el libro
3. Se publica automáticamente en GitHub Pages

### Configurar GitHub Pages

1. Ve a **Settings → Pages**
2. En "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: **gh-pages** (creada automáticamente por el workflow)
   - Folder: **/ (root)**
3. ¡Guarda!

Tu sitio estará disponible en: `https://JR7juanito.github.io/AED`

## ✏️ Cómo editar contenido

1. **Editar un capítulo**: Modifica el archivo `.md` correspondiente en `src/`
2. **Agregar un tema nuevo**:
   - Crea `src/XX-nombre-tema.md`
   - Agrega entrada en `src/SUMMARY.md`
3. **Agregar ejercicios**: Crea archivo en `src/ejercicios/`

Después de cualquier cambio:
```bash
# Compilar localmente para probar
mdbook build

# Ver cambios en vivo
mdbook serve

# Hacer push para desplegar
git add .
git commit -m "Actualizar contenido"
git push
```

## 🔄 Convertir Notebooks a Markdown

Para convertir los archivos `.ipynb` a Markdown, usa:

```bash
# Instalar nbconvert
pip install nbconvert

# Convertir un notebook
jupyter nbconvert --to markdown Archivo.ipynb

# Convertir todos los notebooks
jupyter nbconvert --to markdown *.ipynb
```

Luego copia el contenido markdown a los archivos correspondientes en `src/`.

## 🎨 Personalización

Edita `book.toml` para cambiar:
- `title`: Título del libro
- `author`: Autor
- `description`: Descripción
- Temas, colores, y más

## ❓ Preguntas frecuentes

**P: ¿Cómo agrego imágenes?**
R: Coloca las imágenes en `src/images/` y referencia con `![alt](images/nombre.png)`

**P: ¿Cómo agrego código ejecutable?**
R: Usa bloques de código markdown:
\`\`\`python
print("Hola")
\`\`\`

**P: ¿Cómo cambio el dominio?**
R: Crea archivo `src/CNAME` con tu dominio personalizado.

---

**Para más info sobre mdBook**: https://rust-lang.github.io/mdBook/
