from pdf_to_md_app.utils import build_output_filename, summarize_markdown


def test_build_output_filename_uses_pdf_stem() -> None:
    assert build_output_filename("reporte.final.pdf") == "reporte.final.md"


def test_summarize_markdown_counts_expected_items() -> None:
    markdown = "# Titulo\n\nTexto de ejemplo.\n## Seccion\nMas texto"
    stats = summarize_markdown(markdown)

    assert stats == {
        "lineas": 5,
        "palabras": 9,
        "caracteres": len(markdown),
        "encabezados": 2,
    }
