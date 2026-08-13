from __future__ import annotations

from typing import Any

from .models import VisualEdge, VisualNode, VisualScene


def linked_list_scene(
    nList,
    *,
    field_header: str,
    field_link: str,
    field_data: str,
    str_header: str = "",
    pointers: dict[int, str] | None = None,
) -> VisualScene:
    scene = VisualScene(title="Lista Enlazada")
    pointers = pointers or {}
    node = getattr(nList, field_header)
    idx = 0
    visited: set[int] = set()
    ids = []
    while node is not None:
        marker = id(node)
        if marker in visited:
            loop_id = f"node_loop_{idx}"
            scene.add_node(VisualNode(loop_id, "⟲", shape="circle", width=42, height=42, state="rotating"))
            if ids:
                scene.add_edge(VisualEdge(ids[-1], loop_id, directed=True))
            break
        visited.add(marker)
        node_id = f"node_{idx}"
        label = str(getattr(node, field_data))
        scene.add_node(VisualNode(node_id, label, shape="capsule", width=84, height=44))
        if ids:
            scene.add_edge(VisualEdge(ids[-1], node_id, directed=True))
        ids.append(node_id)
        node = getattr(node, field_link)
        idx += 1

    for pos, label in sorted(pointers.items()):
        if 0 <= pos < len(ids):
            pointer_id = f"pointer_{pos}_{label}"
            scene.add_node(VisualNode(pointer_id, label, shape="rect", width=62, height=34, state="selected"))
            scene.add_edge(VisualEdge(pointer_id, ids[pos], directed=True, state="selected"))

    if str_header and ids:
        header_id = "header"
        scene.add_node(VisualNode(header_id, str_header, shape="rect", width=90, height=36, state="comparing"))
        scene.add_edge(VisualEdge(header_id, ids[0], directed=True))
    return scene


def graph_scene(graph) -> VisualScene:
    scene = VisualScene(title="Grafo")
    nodes = sorted(getattr(graph, "V", []))
    for name in nodes:
        scene.add_node(VisualNode(str(name), str(name), shape="circle", width=52, height=52))
    directed = bool(getattr(graph, "dirigido", False))
    for edge in getattr(graph, "E", []):
        if len(edge) == 2:
            u, v = edge
            w = ""
        else:
            u, v, w = edge
        scene.add_edge(VisualEdge(str(u), str(v), str(w), directed=directed))
    return scene


def array_1d_scene(array, *, show_index: bool = False) -> VisualScene:
    scene = VisualScene(title="Arreglo 1D")
    arr = list(array)
    for i, value in enumerate(arr):
        scene.add_node(VisualNode(f"data_{i}", str(value), shape="rect", width=64, height=42))
        if show_index:
            scene.add_node(
                VisualNode(
                    f"idx_{i}",
                    str(i),
                    shape="rect",
                    width=36,
                    height=28,
                    state="disabled",
                )
            )
    return scene


def array_2d_scene(array, *, show_index: bool = False) -> VisualScene:
    scene = VisualScene(title="Matriz")
    rows = [list(row) for row in array]
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            scene.add_node(VisualNode(f"cell_{i}_{j}", str(value), shape="rect", width=58, height=40))
    if show_index and rows:
        for j in range(len(rows[0])):
            scene.add_node(VisualNode(f"col_{j}", str(j), shape="rect", width=32, height=24, state="disabled"))
        for i in range(len(rows)):
            scene.add_node(VisualNode(f"row_{i}", str(i), shape="rect", width=32, height=24, state="disabled"))
    return scene


def binary_tree_scene(
    tree,
    *,
    root_field: str,
    data_field: str,
    left_field: str,
    right_field: str,
    class_none: type | None = None,
    draw_null: bool = False,
) -> VisualScene:
    scene = VisualScene(title="Árbol Binario")
    root = getattr(tree, root_field)
    counter = {"n": 0}

    def is_empty(node: Any) -> bool:
        if class_none is not None and isinstance(node, class_none):
            return not hasattr(node, data_field)
        return node is None

    def walk(node):
        if is_empty(node):
            if not draw_null:
                return None
            counter["n"] += 1
            null_id = f"null_{counter['n']}"
            scene.add_node(
                VisualNode(null_id, "∅", shape="circle", width=38, height=38, state="disabled")
            )
            return null_id
        counter["n"] += 1
        node_id = f"n_{counter['n']}"
        scene.add_node(
            VisualNode(node_id, str(getattr(node, data_field)), shape="circle", width=52, height=52)
        )
        left_id = walk(getattr(node, left_field))
        right_id = walk(getattr(node, right_field))
        if left_id:
            scene.add_edge(VisualEdge(node_id, left_id, directed=False))
        if right_id:
            scene.add_edge(VisualEdge(node_id, right_id, directed=False))
        return node_id

    root_id = walk(root)
    if root_id is not None:
        scene.metadata["root"] = root_id
    return scene


def tree23_scene(
    tree,
    *,
    class_node2,
    class_node3,
    class_empty,
    fields2=("izq", "info", "der"),
    fields3=("izq", "info1", "med", "info2", "der"),
    field_root="raiz",
    draw_empty=False,
) -> VisualScene:
    scene = VisualScene(title="Árbol 2-3")
    root = getattr(tree, field_root)
    counter = {"n": 0}

    def walk(node):
        if isinstance(node, class_empty):
            if not draw_empty:
                return None
            counter["n"] += 1
            nid = f"e_{counter['n']}"
            scene.add_node(VisualNode(nid, "∅", shape="circle", width=36, height=36, state="disabled"))
            return nid
        counter["n"] += 1
        nid = f"n_{counter['n']}"
        if isinstance(node, class_node2):
            label = str(getattr(node, fields2[1]))
            children = [getattr(node, fields2[0]), getattr(node, fields2[2])]
        elif isinstance(node, class_node3):
            label = f"{getattr(node, fields3[1])} | {getattr(node, fields3[3])}"
            children = [getattr(node, fields3[0]), getattr(node, fields3[2]), getattr(node, fields3[4])]
        else:
            label = "?"
            children = []
        scene.add_node(VisualNode(nid, label, shape="capsule", width=94, height=44))
        for child in children:
            cid = walk(child)
            if cid is not None:
                scene.add_edge(VisualEdge(nid, cid))
        return nid

    root_id = walk(root)
    if root_id is not None:
        scene.metadata["root"] = root_id
    return scene
