from __future__ import annotations

from pathlib import Path


def build_output_filename(pdf_name: str) -> str:
    """Return a predictable markdown filename derived from the PDF name."""
    return f"{Path(pdf_name).stem}.md"


def summarize_markdown(markdown: str) -> dict[str, int]:
    """Compute lightweight markdown stats for the UI."""
    lines = markdown.splitlines()
    headings = sum(1 for line in lines if line.lstrip().startswith("#"))
    words = len(markdown.split())
    characters = len(markdown)
    return {
        "lineas": len(lines),
        "palabras": words,
        "caracteres": characters,
        "encabezados": headings,
    }
