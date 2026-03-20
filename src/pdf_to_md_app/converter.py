from __future__ import annotations

import gc
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile

from pdf_to_md_app.utils import build_output_filename, summarize_markdown


@dataclass
class ConversionResult:
    markdown: str
    output_filename: str
    stats: dict[str, int]
    source_filename: str


def load_models() -> object:
    """Load and return the Marker model artifacts."""
    from marker.models import create_model_dict

    return create_model_dict()


def get_pdf_page_count(filepath: Path) -> int:
    """Return the page count for a PDF file."""
    import pypdfium2 as pdfium

    document = pdfium.PdfDocument(str(filepath))
    try:
        return len(document)
    finally:
        document.close()


def convert_pdf_to_markdown(
    pdf_bytes: bytes,
    source_filename: str,
    artifact_dict: object,
) -> ConversionResult:
    """Convert uploaded PDF bytes into markdown using Marker."""
    from marker.converters.pdf import PdfConverter
    from marker.output import text_from_rendered

    suffix = Path(source_filename).suffix or ".pdf"
    with NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
        temp_path = Path(temp_file.name)
        temp_file.write(pdf_bytes)

    try:
        page_count = get_pdf_page_count(temp_path)
        markdown_parts: list[str] = []

        for page_index in range(page_count):
            converter = PdfConverter(
                artifact_dict=artifact_dict,
                config={"page_range": [page_index]},
            )
            rendered = converter(str(temp_path))
            page_markdown, _, _ = text_from_rendered(rendered)
            cleaned_page_markdown = page_markdown.strip()
            if cleaned_page_markdown:
                markdown_parts.append(cleaned_page_markdown)

            del rendered
            del converter
            gc.collect()

        markdown = "\n\n".join(markdown_parts).strip()
    finally:
        temp_path.unlink(missing_ok=True)

    stats = summarize_markdown(markdown)
    stats["paginas"] = page_count

    return ConversionResult(
        markdown=markdown,
        output_filename=build_output_filename(source_filename),
        stats=stats,
        source_filename=source_filename,
    )
