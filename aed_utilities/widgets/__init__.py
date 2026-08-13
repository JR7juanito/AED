try:
    from IPython.display import Markdown, display
except ModuleNotFoundError:  # pragma: no cover - entorno sin IPython
    Markdown = lambda x: x  # type: ignore

    def display(obj):  # type: ignore
        print(obj)


def _demo_message(name: str):
    display(
        Markdown(
            f"""### {name}

Esta versión está adaptada para JupyterLite + Pyodide.

- Las clases de visualización están disponibles vía `import aed_utilities as aed`.
- Puedes reutilizar tus implementaciones de árboles/listas y llamar sus métodos `draw_*`.
- Esta demo interactiva del paquete original se reemplazó por una guía ligera compatible con web.
"""
        )
    )


def demo_abb():
    _demo_message("Demo ABB")


def demo_abb_root():
    _demo_message("Demo ABB inserción a la raíz")


def demo_avl():
    _demo_message("Demo AVL")


def demo_arbol_23():
    _demo_message("Demo Árbol 2-3")
