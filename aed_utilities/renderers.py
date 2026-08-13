from __future__ import annotations

from html import escape

from .models import VisualNode, VisualScene


STATE_STYLE = {
    "normal": ("#1f2937", "#f8fafc", "#334155"),
    "visiting": ("#92400e", "#fef3c7", "#d97706"),
    "comparing": ("#1e40af", "#dbeafe", "#2563eb"),
    "found": ("#065f46", "#d1fae5", "#10b981"),
    "inserted": ("#166534", "#dcfce7", "#16a34a"),
    "deleted": ("#991b1b", "#fee2e2", "#ef4444"),
    "pivot": ("#7c2d12", "#ffedd5", "#f97316"),
    "rotating": ("#581c87", "#f3e8ff", "#a855f7"),
    "selected": ("#0f172a", "#e2e8f0", "#0f172a"),
    "disabled": ("#6b7280", "#f3f4f6", "#9ca3af"),
}


def _node_style(node: VisualNode):
    return STATE_STYLE.get(node.state, STATE_STYLE["normal"])


def render_text(scene: VisualScene) -> str:
    out = []
    if scene.title:
        out.append(scene.title)
    for node in scene.nodes:
        out.append(f"NODE {node.id} [{node.state}] {node.label}")
    for edge in scene.edges:
        arrow = "->" if edge.directed else "--"
        label = f" ({edge.label})" if edge.label else ""
        out.append(f"EDGE {edge.source} {arrow} {edge.target}{label}")
    return "\n".join(out) if out else "(escena vacía)"


def render_svg(scene: VisualScene) -> str:
    width = int(scene.width or 640)
    height = int(scene.height or 320)
    body = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
        "<defs>",
        '<marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">',
        '<path d="M0,0 L0,6 L9,3 z" fill="#475569"/>',
        "</marker>",
        "</defs>",
        '<rect x="0" y="0" width="100%" height="100%" fill="#ffffff"/>',
    ]
    if scene.title:
        body.append(
            f'<text x="20" y="26" font-family="Inter,Arial,sans-serif" font-size="16" fill="#111827">{escape(scene.title)}</text>'
        )

    for edge in scene.edges:
        source = scene.node_by_id(edge.source)
        target = scene.node_by_id(edge.target)
        if source is None or target is None:
            continue
        body.append(
            '<line '
            f'x1="{source.x:.1f}" y1="{source.y:.1f}" x2="{target.x:.1f}" y2="{target.y:.1f}" '
            'stroke="#475569" stroke-width="2" '
            + ('marker-end="url(#arrow)" ' if edge.directed else "")
            + "/>"
        )
        if edge.label:
            mx = (source.x + target.x) / 2
            my = (source.y + target.y) / 2 - 6
            body.append(
                f'<text x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="12" fill="#0f172a">{escape(str(edge.label))}</text>'
            )

    for node in scene.nodes:
        stroke, fill, text = _node_style(node)
        x = node.x - node.width / 2
        y = node.y - node.height / 2
        if node.shape == "circle":
            r = min(node.width, node.height) / 2
            body.append(
                f'<circle cx="{node.x:.1f}" cy="{node.y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            )
        elif node.shape == "capsule":
            rx = min(node.height / 2, 14)
            body.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{node.width:.1f}" height="{node.height:.1f}" rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            )
        else:
            body.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{node.width:.1f}" height="{node.height:.1f}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            )
        body.append(
            f'<text x="{node.x:.1f}" y="{node.y + 4:.1f}" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="13" fill="{text}">{escape(str(node.label))}</text>'
        )
    body.append("</svg>")
    return "".join(body)
