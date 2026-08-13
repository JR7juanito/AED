from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

try:
    from IPython.display import HTML, display
except ModuleNotFoundError:  # pragma: no cover - entorno sin IPython
    HTML = lambda x: x  # type: ignore

    def display(obj):  # type: ignore
        print(obj)

try:
    import numpy as np
except ModuleNotFoundError:  # pragma: no cover - entorno sin numpy
    np = None


class SegmentationFault(Exception):
    pass


def _render_pre(text: str):
    safe = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    display(HTML(f'<pre style="line-height:1.25em">{safe}</pre>'))


def _render_html(html: str):
    display(HTML(html))


class LinkedListDrawer:
    def __init__(self, **kwargs):
        self.strHeader = kwargs.get("strHeader", "")
        self.fieldLink = kwargs.get("fieldLink", "")
        self.fieldHeader = kwargs.get("fieldHeader", "")
        self.fieldData = kwargs.get("fieldData", "")
        self.fieldReverseLink = kwargs.get("fieldReverseLink", None)
        self.pointers = kwargs.get("pointers", {})

    def draw_linked_list(self, nList):
        p = getattr(nList, self.fieldHeader)
        nodes = []
        seen = set()
        while p is not None:
            if id(p) in seen:
                nodes.append("⟲")
                break
            seen.add(id(p))
            nodes.append(str(getattr(p, self.fieldData)))
            p = getattr(p, self.fieldLink)

        if len(self.pointers) > 0 and max(self.pointers) > len(nodes):
            raise SegmentationFault(
                f"Tried to draw a pointer to node {max(self.pointers)}, but list length is {len(nodes)}."
            )

        head = f"{self.strHeader} → " if self.strHeader else ""
        line = head + " → ".join(f"[{x}]" for x in nodes) + " → ∅"
        if len(nodes) == 0:
            line = head + "∅"

        pointer_lines = []
        for pos, label in sorted(self.pointers.items()):
            if pos < len(nodes):
                pointer_lines.append(f"{label} ↦ [{nodes[pos]}] (posición {pos})")
            else:
                pointer_lines.append(f"{label} ↦ ∅")

        body = line if not pointer_lines else line + "\n" + "\n".join(pointer_lines)
        _render_pre(body)

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
        asc = " ⇄ ".join(str(x) for x in self.ascending_list(nList))
        desc = " ⇄ ".join(str(x) for x in self.descending_list(nList))
        _render_pre(f"Ascendente: {asc}\nDescendente: {desc}")


@dataclass
class _BinaryAsciiNode:
    label: str
    left: "_BinaryAsciiNode | None"
    right: "_BinaryAsciiNode | None"


class BinaryTreeDrawer:
    def __init__(
        self,
        fieldData,
        fieldLeft,
        fieldRight,
        classNone=None,
        drawNull=False,
        shapeInternal="circle",
    ):
        self.nameInfo = fieldData
        self.nameLeft = fieldLeft
        self.nameRight = fieldRight
        self.classNone = classNone
        self.drawNull = drawNull
        self.shapeInternal = shapeInternal

    def _is_empty(self, node: Any) -> bool:
        if self.classNone is not None and isinstance(node, self.classNone):
            return not hasattr(node, self.nameInfo)
        return node is None

    def _copy(self, node: Any):
        if self._is_empty(node):
            if self.drawNull:
                return _BinaryAsciiNode("∅", None, None)
            return None
        return _BinaryAsciiNode(
            str(getattr(node, self.nameInfo)),
            self._copy(getattr(node, self.nameLeft)),
            self._copy(getattr(node, self.nameRight)),
        )

    def _lines(self, node: _BinaryAsciiNode | None, prefix: str = "", is_left: bool = True):
        if node is None:
            return []
        branch = "└── " if is_left else "┌── "
        lines = [prefix + branch + node.label]
        child_prefix = prefix + ("    " if is_left else "│   ")
        lines.extend(self._lines(node.right, child_prefix, False))
        lines.extend(self._lines(node.left, child_prefix, True))
        return lines

    def draw_tree(self, tree, root):
        node = self._copy(getattr(tree, root))
        if node is None:
            _render_pre("∅")
            return
        _render_pre("\n".join(self._lines(node)))


class GraphDrawer:
    def __init__(self):
        pass

    def draw_graph(self, graph):
        connector = "→" if graph.dirigido else "—"
        rows = []
        for edge in graph.E:
            if len(edge) == 2:
                u, v = edge
                rows.append(f"{u} {connector} {v}")
            else:
                u, v, w = edge
                rows.append(f"{u} {connector} {v}  (peso={w})")
        _render_pre("\n".join(rows) if rows else "(grafo vacío)")


class NumpyArrayDrawer:
    def __init__(self, animation=False):
        self.animation = animation

    def drawNumpy1DArray(self, array, showIndex=False, layout="row"):
        arr = np.asarray(array).tolist() if np is not None else list(array)
        if len(arr) > 0 and isinstance(arr[0], (list, tuple)):
            raise ValueError("drawNumpy1DArray espera un arreglo de una dimensión.")

        if layout == "column":
            rows = []
            for i, x in enumerate(arr):
                if showIndex:
                    rows.append(f"<tr><td>{i}</td><td>{x}</td></tr>")
                else:
                    rows.append(f"<tr><td>{x}</td></tr>")
            html = (
                '<table border="1" style="border-collapse:collapse;text-align:center;">'
                + "".join(rows)
                + "</table>"
            )
        else:
            data_row = "".join(f"<td>{x}</td>" for x in arr)
            index_row = "".join(f"<td>{i}</td>" for i in range(len(arr)))
            html = (
                '<table border="1" style="border-collapse:collapse;text-align:center;">'
                f"<tr>{data_row}</tr>"
                + (f"<tr>{index_row}</tr>" if showIndex else "")
                + "</table>"
            )

        if self.animation:
            return html
        _render_html(html)
        return None

    def drawNumpy2DArray(self, array, showIndex=False):
        arr = np.asarray(array).tolist() if np is not None else [list(row) for row in array]
        if len(arr) == 0:
            _render_html('<table border="1" style="border-collapse:collapse;text-align:center;"></table>')
            return None
        if not isinstance(arr[0], (list, tuple)):
            raise ValueError("drawNumpy2DArray espera un arreglo de dos dimensiones.")

        rows = []
        if showIndex:
            top = "<tr><td></td>" + "".join(f"<td>{j}</td>" for j in range(len(arr[0]))) + "</tr>"
            rows.append(top)

        for i in range(len(arr)):
            row_vals = "".join(f"<td>{arr[i][j]}</td>" for j in range(len(arr[i])))
            if showIndex:
                rows.append(f"<tr><td>{i}</td>{row_vals}</tr>")
            else:
                rows.append(f"<tr>{row_vals}</tr>")

        html = (
            '<table border="1" style="border-collapse:collapse;text-align:center;">'
            + "".join(rows)
            + "</table>"
        )
        if self.animation:
            return html
        _render_html(html)
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

    def _draw(self, node, prefix="", tail=True):
        if isinstance(node, self.classEmpty) and not self.drawEmpty:
            return []
        lines = [f"{prefix}{'└── ' if tail else '├── '}{self._label(node)}"]
        children = [c for c in self._children(node) if not isinstance(c, self.classEmpty) or self.drawEmpty]
        for i, child in enumerate(children):
            nxt = prefix + ("    " if tail else "│   ")
            lines.extend(self._draw(child, nxt, i == len(children) - 1))
        return lines

    def draw_tree(self, tree):
        root = getattr(tree, self.fieldRoot)
        if isinstance(root, self.classEmpty) and not self.drawEmpty:
            _render_pre("∅")
            return
        _render_pre("\n".join(self._draw(root)))
