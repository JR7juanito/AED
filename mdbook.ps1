# Helper scripts para mdBook en Windows

param(
    [Parameter(Position=0)]
    [string]$Command = ""
)

switch ($Command) {
    "install" {
        Write-Host "📦 Instalando mdBook..." -ForegroundColor Green
        cargo install mdbook
        Write-Host "✓ mdBook instalado" -ForegroundColor Green
    }
    "build" {
        Write-Host "🔨 Compilando libro..." -ForegroundColor Green
        mdbook build
        Write-Host "✓ Libro compilado en ./book/" -ForegroundColor Green
    }
    "serve" {
        Write-Host "🚀 Iniciando servidor local..." -ForegroundColor Green
        Write-Host "📖 Abre http://localhost:3000" -ForegroundColor Green
        mdbook serve
    }
    "convert" {
        Write-Host "🔄 Convirtiendo notebooks a markdown..." -ForegroundColor Green
        python convert_notebooks.py
    }
    "clean" {
        Write-Host "🧹 Limpiando archivos compilados..." -ForegroundColor Green
        if (Test-Path ".\book") {
            Remove-Item -Recurse -Force ".\book"
        }
        Write-Host "✓ Limpeza completada" -ForegroundColor Green
    }
    "watch" {
        Write-Host "👁️  Vigilando cambios..." -ForegroundColor Green
        mdbook watch
    }
    default {
        Write-Host "Uso: .\mdbook.ps1 [comando]" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Comandos disponibles:" -ForegroundColor Green
        Write-Host "  install   - Instalar mdBook"
        Write-Host "  build     - Compilar el libro"
        Write-Host "  serve     - Iniciar servidor local (localhost:3000)"
        Write-Host "  convert   - Convertir notebooks a markdown"
        Write-Host "  clean     - Limpiar archivos compilados"
        Write-Host "  watch     - Vigilar cambios automáticamente"
        Write-Host ""
        Write-Host "Ejemplo: .\mdbook.ps1 serve" -ForegroundColor Green
    }
}
