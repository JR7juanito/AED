from __future__ import annotations

try:
    from IPython.display import HTML, Markdown, display
except ModuleNotFoundError:  # pragma: no cover
    HTML = lambda x: x  # type: ignore
    Markdown = lambda x: x  # type: ignore

    def display(obj):  # type: ignore
        print(obj)


def show_svg(svg: str):
    display(HTML(svg))


def show_text(text: str):
    display(HTML(f"<pre>{text}</pre>"))


def show_markdown(md: str):
    display(Markdown(md))
