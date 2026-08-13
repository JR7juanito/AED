from __future__ import annotations

from typing import Any, Iterable

try:
    import numpy as np
except ModuleNotFoundError:  # pragma: no cover
    np = None

from .adapters import (
    array_1d_scene,
    array_2d_scene,
    binary_tree_scene,
    graph_scene,
    linked_list_scene,
    tree23_scene,
)
from .display import show_svg, show_text
from .layouts import (
    fit_scene,
    layout_binary_tree,
    layout_circular,
    layout_general_tree,
    layout_grid,
    layout_linear,
)
from .models import VisualEdge
from .renderers import render_svg, render_text


class SegmentationFault(Exception):
    pass


def _render_scene(scene, renderer: str = "svg"):
    if renderer == "text":
        text = render_text(scene)
        show_text(text)
        return text
    svg = render_svg(scene)
    show_svg(svg)
    return svg


class LinkedListDrawer:
    def __init__(self, **kwargs):
        self.strHeader = kwargs.get("strHeader", "")
        self.fieldLink = kwargs.get("fieldLink", "")
        self.fieldHeader = kwargs.get("fieldHeader", "")
        self.fieldData = kwargs.get("fieldData", "")
        self.fieldReverseLink = kwargs.get("fieldReverseLink", None)
        self.pointers = kwargs.get("pointers", {})
        self.renderer = kwargs.get("renderer", "svg")

    def draw_linked_list(self, nList):
        scene = linked_list_scene(
            nList,
            field_header=self.fieldHeader,
            field_link=self.fieldLink,
            field_data=self.fieldData,
            str_header=self.strHeader,
            pointers=self.pointers,
        )
        pointer_nodes = [n for n in scene.nodes if n.id.startswith("pointer_")]
        layout_linear(scene)
        if pointer_nodes:
            data_nodes = [n for n in scene.nodes if n.id.startswith("node_")]
            y_above = min((n.y for n in data_nodes), default=80) - 56
            for p in pointer_nodes:
                pos = int(p.id.split("_")[1])
                target = scene.node_by_id(f"node_{pos}")
                if target is not None:
                    p.x = target.x
                    p.y = y_above
            fit_scene(scene)
        _render_scene(scene, self.renderer)

    def ascending_list(self, nList):
        p = getattr(getattr(nList, self.fieldHeader), self.fieldLink)
        while p is not getattr(nList, self.fieldHeader):
            yield getattr(p, self.fieldData)
            p = getattr(p, self.fieldLink)

    def descending_list(self, nList):
        p = getattr(getattr(nList, self.fieldHeader), self.fieldReverseLink)
        while p is not getattr(nList, self.fieldHeader):
            yield getattr(p, self.fieldData)
            p = getattr(p, self.fieldReverseLink)

    def draw_double_linked_list(self, nList):
        values = list(self.ascending_list(nList))
        scene = array_1d_scene(values)
        scene.title = "Lista Doblemente Enlazada"
        for edge in scene.edges:
            edge.directed = True
        for i in range(1, len(values)):
            scene.add_edge(VisualEdge(f"data_{i}", f"data_{i-1}", directed=True))
        layout_linear(scene)
        _render_scene(scene, self.renderer)


class BinaryTreeDrawer:
    def __init__(
        self,
        fieldData,
        fieldLeft,
        fieldRight,
        classNone=None,
        drawNull=False,
        shapeInternal="circle",
        renderer="svg",
    ):
        self.nameInfo = fieldData
        self.nameLeft = fieldLeft
        self.nameRight = fieldRight
        self.classNone = classNone
        self.drawNull = drawNull
        self.shapeInternal = shapeInternal
        self.renderer = renderer

    def draw_tree(self, tree, root):
        scene = binary_tree_scene(
            tree,
            root_field=root,
            data_field=self.nameInfo,
            left_field=self.nameLeft,
            right_field=self.nameRight,
            class_none=self.classNone,
            draw_null=self.drawNull,
        )
        for node in scene.nodes:
            if node.shape != "circle":
                continue
            node.shape = self.shapeInternal if self.shapeInternal in ("circle", "rect", "capsule") else "circle"
        layout_binary_tree(scene, scene.metadata.get("root", ""))
        _render_scene(scene, self.renderer)


class GraphDrawer:
    def __init__(self, renderer="svg"):
        self.renderer = renderer

    def draw_graph(self, graph):
        scene = graph_scene(graph)
        layout_circular(scene)
        _render_scene(scene, self.renderer)


class NumpyArrayDrawer:
    def __init__(self, animation=False, renderer="svg"):
        self.animation = animation
        self.renderer = renderer

    def drawNumpy1DArray(self, array, showIndex=False, layout="row"):
        arr = np.asarray(array).tolist() if np is not None else list(array)
        if len(arr) > 0 and isinstance(arr[0], (list, tuple)):
            raise ValueError("drawNumpy1DArray espera un arreglo de una dimensión.")
        scene = array_1d_scene(arr, show_index=showIndex)
        if layout == "column":
            data_nodes = [n for n in scene.nodes if n.id.startswith("data_")]
            for node in data_nodes:
                idx = int(node.id.split("_")[1])
                node.x = 80
                node.y = 70 + idx * 62
            if showIndex:
                for node in scene.nodes:
                    if node.id.startswith("idx_"):
                        idx = int(node.id.split("_")[1])
                        node.x = 28
                        node.y = 70 + idx * 62
            fit_scene(scene)
        else:
            layout_linear(scene, spacing=76)
            if showIndex:
                for node in scene.nodes:
                    if node.id.startswith("idx_"):
                        idx = int(node.id.split("_")[1])
                        data_node = scene.node_by_id(f"data_{idx}")
                        if data_node:
                            node.x = data_node.x
                            node.y = data_node.y + 36
                fit_scene(scene)

        rendered = _render_scene(scene, self.renderer)
        if self.animation:
            return rendered
        return None

    def drawNumpy2DArray(self, array, showIndex=False):
        arr = np.asarray(array).tolist() if np is not None else [list(row) for row in array]
        if len(arr) == 0:
            scene = array_2d_scene([], show_index=showIndex)
            layout_grid(scene, cols=1)
            rendered = _render_scene(scene, self.renderer)
            if self.animation:
                return rendered
            return None
        if not isinstance(arr[0], (list, tuple)):
            raise ValueError("drawNumpy2DArray espera un arreglo de dos dimensiones.")

        scene = array_2d_scene(arr, show_index=showIndex)
        cols = len(arr[0]) if arr else 1
        for node in scene.nodes:
            if node.id.startswith("cell_"):
                _, i, j = node.id.split("_")
                node.x = 70 + int(j) * 70
                node.y = 70 + int(i) * 56
            elif node.id.startswith("col_"):
                j = int(node.id.split("_")[1])
                node.x = 70 + j * 70
                node.y = 28
            elif node.id.startswith("row_"):
                i = int(node.id.split("_")[1])
                node.x = 26
                node.y = 70 + i * 56
        fit_scene(scene)
        rendered = _render_scene(scene, self.renderer)
        if self.animation:
            return rendered
        return None


class Tree23Drawer:
    def __init__(
        self,
        classNode2,
        classNode3,
        classEmpty,
        fields2=("izq", "info", "der"),
        fields3=("izq", "info1", "med", "info2", "der"),
        fieldRoot="raiz",
        shape2="circle",
        shape3="Mrecord",
        drawEmpty=False,
        renderer="svg",
    ):
        self.classNode2 = classNode2
        self.classNode3 = classNode3
        self.classEmpty = classEmpty
        self.fields2 = fields2
        self.fields3 = fields3
        self.fieldRoot = fieldRoot
        self.shape2 = shape2
        self.shape3 = shape3
        self.drawEmpty = drawEmpty
        self.renderer = renderer

    def _label(self, node):
        if isinstance(node, self.classEmpty):
            return "∅"
        if isinstance(node, self.classNode2):
            return str(getattr(node, self.fields2[1]))
        if isinstance(node, self.classNode3):
            return f"{getattr(node, self.fields3[1])} | {getattr(node, self.fields3[3])}"
        return "?"

    def _children(self, node) -> Iterable[Any]:
        if isinstance(node, self.classNode2):
            return [getattr(node, self.fields2[0]), getattr(node, self.fields2[2])]
        if isinstance(node, self.classNode3):
            return [
                getattr(node, self.fields3[0]),
                getattr(node, self.fields3[2]),
                getattr(node, self.fields3[4]),
            ]
        return []

    def draw_tree(self, tree):
        scene = tree23_scene(
            tree,
            class_node2=self.classNode2,
            class_node3=self.classNode3,
            class_empty=self.classEmpty,
            fields2=self.fields2,
            fields3=self.fields3,
            field_root=self.fieldRoot,
            draw_empty=self.drawEmpty,
        )
        layout_general_tree(scene, scene.metadata.get("root", ""))
        _render_scene(scene, self.renderer)
