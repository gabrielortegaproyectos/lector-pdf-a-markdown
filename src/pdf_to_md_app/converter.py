from __future__ import annotations

import asyncio
import os
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


def load_api_key(explicit_api_key: str | None = None) -> str:
    """Resolve the Llama Cloud API key from an explicit value or the environment."""
    api_key = explicit_api_key or os.getenv("LLAMA_CLOUD_API_KEY", "")
    if not api_key:
        raise ValueError(
            "No se encontró LLAMA_CLOUD_API_KEY. Configúrala en variables de entorno, "
            "en Streamlit Secrets o ingrésala en la interfaz."
        )
    return api_key


async def parse_pdf_with_llamaparse(filepath: Path, api_key: str) -> tuple[str, int]:
    """Upload a PDF to LlamaParse and return merged markdown plus page count."""
    from llama_cloud import AsyncLlamaCloud

    os.environ["LLAMA_CLOUD_API_KEY"] = api_key
    client = AsyncLlamaCloud()

    uploaded_file = await client.files.create(file=str(filepath), purpose="parse")
    result = await client.parsing.parse(
        file_id=uploaded_file.id,
        tier="agentic",
        version="latest",
        expand=["markdown"],
    )

    pages = getattr(getattr(result, "markdown", None), "pages", []) or []
    markdown_parts = [
        getattr(page, "markdown", "").strip()
        for page in pages
        if getattr(page, "markdown", "").strip()
    ]
    markdown = "\n\n".join(markdown_parts).strip()
    return markdown, len(pages)


def convert_pdf_to_markdown(
    pdf_bytes: bytes,
    source_filename: str,
    api_key: str | None = None,
) -> ConversionResult:
    """Convert uploaded PDF bytes into markdown using LlamaParse."""
    resolved_api_key = load_api_key(api_key)

    suffix = Path(source_filename).suffix or ".pdf"
    with NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
        temp_path = Path(temp_file.name)
        temp_file.write(pdf_bytes)

    try:
        markdown, page_count = asyncio.run(
            parse_pdf_with_llamaparse(temp_path, resolved_api_key)
        )
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
