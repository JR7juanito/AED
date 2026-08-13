from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class VisualNode:
    id: str
    label: str
    x: float = 0.0
    y: float = 0.0
    width: float = 80.0
    height: float = 44.0
    shape: str = "rect"
    state: str = "normal"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class VisualEdge:
    source: str
    target: str
    label: str = ""
    directed: bool = False
    state: str = "normal"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class VisualScene:
    nodes: list[VisualNode] = field(default_factory=list)
    edges: list[VisualEdge] = field(default_factory=list)
    width: float = 0.0
    height: float = 0.0
    title: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_node(self, node: VisualNode):
        self.nodes.append(node)

    def add_edge(self, edge: VisualEdge):
        self.edges.append(edge)

    def node_by_id(self, node_id: str) -> VisualNode | None:
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None
