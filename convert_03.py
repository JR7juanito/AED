import json
import glob
from pathlib import Path

# Encontrar el archivo exacto
files = glob.glob('03*.ipynb')
if files:
    notebook = files[0]
    output = 'src/03-diseño-algoritmos.md'
    
    print(f'Procesando: {notebook}')
    with open(notebook, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    content = []
    for cell in nb.get('cells', []):
        cell_type = cell.get('cell_type')
        
        if cell_type == 'markdown':
            source = ''.join(cell.get('source', []))
            if source.strip():
                content.append(source)
                
        elif cell_type == 'code':
            source = ''.join(cell.get('source', []))
            if source.strip():
                content.append(f'\n```python\n{source}\n```\n')
    
    markdown_content = '\n'.join(content)
    
    with open(output, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f'✓ Convertido a {output}')
else:
    print('No encontrado')
