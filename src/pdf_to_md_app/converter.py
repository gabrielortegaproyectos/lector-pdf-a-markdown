from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile

from pdf_to_md_app.utils import build_output_filename, summarize_markdown

DAILY_PAGE_LIMIT = 900
DEFAULT_LLAMA_CLOUD_API_KEY = "llx-SFbXa56TQXvMwpISu0YSzp3Eyp0lkd3j9yqCGFwgHmylpFKT"


@dataclass
class ConversionResult:
    markdown: str
    output_filename: str
    stats: dict[str, int]
    source_filename: str
    images: list[dict[str, str]]


def load_api_key(explicit_api_key: str | None = None) -> str:
    """Resolve the Llama Cloud API key from an explicit value or the environment."""
    api_key = explicit_api_key or os.getenv("LLAMA_CLOUD_API_KEY", "") or DEFAULT_LLAMA_CLOUD_API_KEY
    if not api_key:
        raise ValueError("La aplicación no tiene configurada la credencial del servidor.")
    return api_key


def get_pdf_page_count(pdf_bytes: bytes) -> int:
    """Count pages in an uploaded PDF."""
    from pypdf import PdfReader

    reader = PdfReader(BytesIO(pdf_bytes))
    return len(reader.pages)


async def parse_pdf_with_llamaparse(filepath: Path, api_key: str) -> tuple[str, int, list[dict[str, str]]]:
    """Upload a PDF to LlamaParse and return merged markdown, page count, and image links."""
    from llama_cloud import AsyncLlamaCloud

    os.environ["LLAMA_CLOUD_API_KEY"] = api_key
    client = AsyncLlamaCloud()

    uploaded_file = await client.files.create(file=str(filepath), purpose="parse")
    job = await client.parsing.create(
        file_id=uploaded_file.id,
        tier="agentic",
        version="latest",
        output_options={
            "images_to_save": ["embedded", "layout"],
        },
        page_ranges={
            "max_pages": DAILY_PAGE_LIMIT,
        },
    )
    result = await client.parsing.get(
        job.id,
        expand=["markdown", "images_content_metadata"],
    )

    pages = getattr(getattr(result, "markdown", None), "pages", []) or []
    markdown_parts = [
        getattr(page, "markdown", "").strip()
        for page in pages
        if getattr(page, "markdown", "").strip()
    ]
    markdown = "\n\n".join(markdown_parts).strip()
    image_entries = []
    images_metadata = getattr(result, "images_content_metadata", None)
    if images_metadata:
        for image in getattr(images_metadata, "images", []) or []:
            presigned_url = getattr(image, "presigned_url", None)
            if not presigned_url:
                continue
            image_entries.append(
                {
                    "filename": getattr(image, "filename", "imagen"),
                    "url": presigned_url,
                    "category": getattr(image, "category", "embedded") or "embedded",
                }
            )
    return markdown, len(pages), image_entries


def convert_pdf_to_markdown(
    pdf_bytes: bytes,
    source_filename: str,
    api_key: str | None = None,
) -> ConversionResult:
    """Convert uploaded PDF bytes into markdown using LlamaParse."""
    resolved_api_key = load_api_key(api_key)
    page_count = get_pdf_page_count(pdf_bytes)
    if page_count > DAILY_PAGE_LIMIT:
        raise ValueError(
            f"El documento tiene {page_count} páginas y supera el límite diario de {DAILY_PAGE_LIMIT} páginas."
        )

    suffix = Path(source_filename).suffix or ".pdf"
    with NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
        temp_path = Path(temp_file.name)
        temp_file.write(pdf_bytes)

    try:
        markdown, parsed_pages, images = asyncio.run(
            parse_pdf_with_llamaparse(temp_path, resolved_api_key)
        )
    finally:
        temp_path.unlink(missing_ok=True)

    stats = summarize_markdown(markdown)
    stats["paginas"] = parsed_pages

    return ConversionResult(
        markdown=markdown,
        output_filename=build_output_filename(source_filename),
        stats=stats,
        source_filename=source_filename,
        images=images,
    )
