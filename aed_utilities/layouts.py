from __future__ import annotations

import math
from collections import defaultdict, deque

from .models import VisualScene


def fit_scene(scene: VisualScene, padding: float = 32):
    if not scene.nodes:
        scene.width = 320
        scene.height = 120
        return

    min_x = min(node.x - node.width / 2 for node in scene.nodes)
    max_x = max(node.x + node.width / 2 for node in scene.nodes)
    min_y = min(node.y - node.height / 2 for node in scene.nodes)
    max_y = max(node.y + node.height / 2 for node in scene.nodes)
    dx = padding - min_x
    dy = padding - min_y
    for node in scene.nodes:
        node.x += dx
        node.y += dy
    scene.width = max_x - min_x + 2 * padding
    scene.height = max_y - min_y + 2 * padding


def layout_linear(scene: VisualScene, spacing: float = 110, y: float = 80):
    for idx, node in enumerate(scene.nodes):
        node.x = 60 + idx * spacing
        node.y = y
    fit_scene(scene)


def layout_grid(scene: VisualScene, cols: int, cell_w: float = 84, cell_h: float = 54, start_y: float = 80):
    cols = max(cols, 1)
    for idx, node in enumerate(scene.nodes):
        row = idx // cols
        col = idx % cols
        node.x = 60 + col * cell_w
        node.y = start_y + row * cell_h
    fit_scene(scene)


def layout_circular(scene: VisualScene, radius: float = 120):
    n = len(scene.nodes)
    if n == 0:
        fit_scene(scene)
        return
    if n == 1:
        scene.nodes[0].x = 120
        scene.nodes[0].y = 120
        fit_scene(scene)
        return
    for i, node in enumerate(scene.nodes):
        angle = (2 * math.pi * i / n) - math.pi / 2
        node.x = 180 + radius * math.cos(angle)
        node.y = 180 + radius * math.sin(angle)
    fit_scene(scene)


def layout_binary_tree(scene: VisualScene, root_id: str):
    root = scene.node_by_id(root_id)
    if root is None:
        fit_scene(scene)
        return

    children = defaultdict(list)
    for edge in scene.edges:
        children[edge.source].append(edge.target)

    positions = {}
    x_counter = [0]

    def walk(node_id: str, depth: int):
        kids = children.get(node_id, [])
        if not kids:
            x_counter[0] += 1
            positions[node_id] = (x_counter[0], depth)
            return
        if len(kids) >= 1:
            walk(kids[0], depth + 1)
        if len(kids) == 1:
            x_counter[0] += 1
            positions[node_id] = (x_counter[0], depth)
        else:
            walk(kids[1], depth + 1)
            lx = positions[kids[0]][0]
            rx = positions[kids[1]][0]
            positions[node_id] = ((lx + rx) / 2, depth)

    walk(root_id, 0)

    for node in scene.nodes:
        px, py = positions.get(node.id, (0, 0))
        node.x = 70 + px * 95
        node.y = 60 + py * 90
    fit_scene(scene)


def layout_general_tree(scene: VisualScene, root_id: str):
    root = scene.node_by_id(root_id)
    if root is None:
        fit_scene(scene)
        return

    children = defaultdict(list)
    for edge in scene.edges:
        children[edge.source].append(edge.target)

    levels: list[list[str]] = []
    q = deque([(root_id, 0)])
    visited = set()
    while q:
        node_id, depth = q.popleft()
        if node_id in visited:
            continue
        visited.add(node_id)
        while len(levels) <= depth:
            levels.append([])
        levels[depth].append(node_id)
        for child in children.get(node_id, []):
            q.append((child, depth + 1))

    y_step = 90
    for depth, level_ids in enumerate(levels):
        x_step = 110
        offset = 70
        for idx, node_id in enumerate(level_ids):
            node = scene.node_by_id(node_id)
            if node is None:
                continue
            node.x = offset + idx * x_step
            node.y = 60 + depth * y_step
    fit_scene(scene)
