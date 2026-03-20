from __future__ import annotations

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
        converter = PdfConverter(artifact_dict=artifact_dict)
        rendered = converter(str(temp_path))
        markdown, _, _ = text_from_rendered(rendered)
    finally:
        temp_path.unlink(missing_ok=True)

    return ConversionResult(
        markdown=markdown,
        output_filename=build_output_filename(source_filename),
        stats=summarize_markdown(markdown),
        source_filename=source_filename,
    )
