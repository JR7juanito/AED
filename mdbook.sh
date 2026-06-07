#!/bin/bash
# Helper scripts para mdBook

case "${1}" in
  install)
    echo "📦 Instalando mdBook..."
    cargo install mdbook
    echo "✓ mdBook instalado"
    ;;
  build)
    echo "🔨 Compilando libro..."
    mdbook build
    echo "✓ Libro compilado en ./book/"
    ;;
  serve)
    echo "🚀 Iniciando servidor local..."
    echo "📖 Abre http://localhost:3000"
    mdbook serve
    ;;
  convert)
    echo "🔄 Convirtiendo notebooks a markdown..."
    python convert_notebooks.py
    ;;
  clean)
    echo "🧹 Limpiando archivos compilados..."
    rm -rf book/
    echo "✓ Limpeza completada"
    ;;
  watch)
    echo "👁️  Vigilando cambios..."
    mdbook watch
    ;;
  *)
    echo "Uso: ./mdbook.sh [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  install   - Instalar mdBook"
    echo "  build     - Compilar el libro"
    echo "  serve     - Iniciar servidor local (localhost:3000)"
    echo "  convert   - Convertir notebooks a markdown"
    echo "  clean     - Limpiar archivos compilados"
    echo "  watch     - Vigilar cambios automáticamente"
    echo ""
    echo "Ejemplo: ./mdbook.sh serve"
    ;;
esac
