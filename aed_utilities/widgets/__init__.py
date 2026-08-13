from __future__ import annotations

from dataclasses import dataclass

from ..display import show_markdown
from ..models import VisualNode
from ..visualizacion import BinaryTreeDrawer

try:
    import ipywidgets as widgets
    from IPython.display import display
except ModuleNotFoundError:  # pragma: no cover
    widgets = None

    def display(obj):  # type: ignore
        print(obj)


@dataclass
class _Node:
    info: int
    izq: "_Node | None" = None
    der: "_Node | None" = None


class _Tree:
    def __init__(self, raiz):
        self.raiz = raiz


def _sample_tree():
    return _Tree(
        _Node(
            8,
            _Node(4, _Node(2), _Node(6)),
            _Node(12, _Node(10), _Node(14)),
        )
    )


def _render_tree_with_state(renderer: str, state: str, value: int):
    drawer = BinaryTreeDrawer(
        fieldData="info",
        fieldLeft="izq",
        fieldRight="der",
        drawNull=False,
        renderer=renderer,
    )
    tree = _sample_tree()

    from ..adapters import binary_tree_scene
    from ..layouts import layout_binary_tree
    from ..renderers import render_svg
    from ..display import show_svg

    scene = binary_tree_scene(
        tree,
        root_field="raiz",
        data_field="info",
        left_field="izq",
        right_field="der",
        draw_null=False,
    )
    for node in scene.nodes:
        if node.label == str(value):
            node.state = state
    layout_binary_tree(scene, scene.metadata.get("root", ""))
    if renderer == "text":
        drawer.draw_tree(tree, "raiz")
    else:
        show_svg(render_svg(scene))


def _widget_demo(title: str):
    if widgets is None:
        show_markdown(
            f"""### {title}

ipywidgets no está disponible en este entorno.

- Puedes usar los drawers directamente con `renderer="svg"` (predeterminado).
- Fallback de texto disponible con `renderer="text"`.
"""
        )
        return

    renderer = widgets.Dropdown(options=["svg", "text"], value="svg", description="Renderer")
    node_value = widgets.SelectionSlider(
        options=[2, 4, 6, 8, 10, 12, 14],
        value=8,
        description="Nodo",
        continuous_update=False,
    )
    state = widgets.Dropdown(
        options=["normal", "visiting", "comparing", "found", "inserted", "pivot", "rotating", "selected"],
        value="found",
        description="Estado",
    )
    output = widgets.Output()

    def refresh(*_):
        with output:
            output.clear_output()
            _render_tree_with_state(renderer.value, state.value, int(node_value.value))

    renderer.observe(refresh, names="value")
    node_value.observe(refresh, names="value")
    state.observe(refresh, names="value")
    display(widgets.VBox([widgets.HTML(f"<h4>{title}</h4>"), widgets.HBox([renderer, node_value, state]), output]))
    refresh()


def demo_abb():
    _widget_demo("Demo ABB Interactiva")


def demo_abb_root():
    _widget_demo("Demo ABB Inserción a la Raíz")


def demo_avl():
    _widget_demo("Demo AVL (estados visuales)")


def demo_arbol_23():
    _widget_demo("Demo Árbol 2-3 (estados visuales)")
