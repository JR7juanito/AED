#!/usr/bin/env python3
"""
Script para convertir Jupyter Notebooks a Markdown para mdBook.
Requiere: pip install nbconvert
"""

import json
import os
import sys
import glob
from pathlib import Path


def extract_notebook_cells(notebook_path):
    """Extrae contenido de celdas markdown y código de un notebook."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    content = []
    for cell in nb.get('cells', []):
        cell_type = cell.get('cell_type')
        
        if cell_type == 'markdown':
            # Procesar celdas markdown
            source = ''.join(cell.get('source', []))
            if source.strip():
                content.append(source)
                
        elif cell_type == 'code':
            # Procesar celdas de código
            source = ''.join(cell.get('source', []))
            if source.strip():
                content.append(f"\n```python\n{source}\n```\n")
                
                # Si hay output, también lo incluimos
                outputs = cell.get('outputs', [])
                for output in outputs:
                    if output.get('output_type') == 'stream':
                        text = ''.join(output.get('text', []))
                        if text.strip():
                            content.append(f"\n```\n{text}\n```\n")
                    elif output.get('output_type') == 'execute_result':
                        data = output.get('data', {})
                        if 'text/plain' in data:
                            text = ''.join(data['text/plain'])
                            if text.strip():
                                content.append(f"\n```\nResultado:\n{text}\n```\n")
    
    return '\n'.join(content)


def convert_notebook(notebook_path, output_path):
    """Convierte un notebook a archivo markdown."""
    try:
        markdown_content = extract_notebook_cells(notebook_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✓ Convertido: {notebook_path} → {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error procesando {notebook_path}: {e}")
        return False


def main():
    """Convierte todos los notebooks del proyecto."""
    
    # Mapeo de notebooks a archivos markdown de destino
    notebook_mappings = {
        '01_Introduccion.ipynb': 'src/01-introduccion.md',
        '02_Metodos_Matematicos_para_el_Analisis_de_Algoritmos.ipynb': 'src/02-metodos-matematicos.md',
        '03_Diseño_de_Algoritmos_Eficientes.ipynb': 'src/03-diseño-algoritmos.md',
        '03_Diseño_de_Algoritmos_Eficientes.ipynb': 'src/03-diseño-algoritmos.md',  # Alternativa con encoding
        '04_Estructuras_de_Datos_Elementales.ipynb': 'src/04-estructuras-datos.md',
        '05_Pilas_Colas_y_Colas_de_Prioridad.ipynb': 'src/05-pilas-colas.md',
        '06_Diccionarios.ipynb': 'src/06-diccionarios.md',
        '07_Ordenacion.ipynb': 'src/07-ordenacion.md',
        '08_Busqueda_en_Texto.ipynb': 'src/08-busqueda-texto.md',
        '09_Compresion_de_Datos.ipynb': 'src/09-compresion-datos.md',
        '10_Grafos.ipynb': 'src/10-grafos.md',
    }
    
    # Mapeo de ejercicios
    exercise_mappings = {
        'Ejercicios/01_Ejercicios.ipynb': 'src/ejercicios/01-ejercicios.md',
        'Ejercicios/02_Ejercicios.ipynb': 'src/ejercicios/02-ejercicios.md',
        'Ejercicios/03_Ejercicios.ipynb': 'src/ejercicios/03-ejercicios.md',
        'Ejercicios/04_Ejercicios.ipynb': 'src/ejercicios/04-ejercicios.md',
        'Ejercicios/05_Ejercicios.ipynb': 'src/ejercicios/05-ejercicios.md',
        'Ejercicios/06_Ejercicios.ipynb': 'src/ejercicios/06-ejercicios.md',
        'Ejercicios/07_Ejercicios.ipynb': 'src/ejercicios/07-ejercicios.md',
    }
    
    print("🔄 Iniciando conversión de Notebooks a Markdown...\n")
    
    # Convertir notebooks principales
    print("📚 Convirtiendo apuntes:")
    converted = 0
    for notebook, output in notebook_mappings.items():
        if Path(notebook).exists():
            if convert_notebook(notebook, output):
                converted += 1
        else:
            print(f"  ⚠ No encontrado: {notebook}")
    
    print(f"\n✓ {converted}/{len(notebook_mappings)} apuntes convertidos")
    
    # Convertir ejercicios
    print("\n📝 Convirtiendo ejercicios:")
    converted = 0
    for notebook, output in exercise_mappings.items():
        if Path(notebook).exists():
            if convert_notebook(notebook, output):
                converted += 1
        else:
            print(f"  ⚠ No encontrado: {notebook}")
    
    print(f"\n✓ {converted}/{len(exercise_mappings)} ejercicios convertidos")
    print("\n✨ ¡Conversión completada!")
    print("\nPróximos pasos:")
    print("  1. Revisa los archivos markdown generados")
    print("  2. Mejora el formato si es necesario")
    print("  3. Agrega imágenes desde la carpeta 'recursos/'")
    print("  4. Compila con: mdbook build")
    print("  5. Revisa con: mdbook serve")
    print("  6. Haz push a GitHub para desplegar automáticamente")


if __name__ == '__main__':
    main()
