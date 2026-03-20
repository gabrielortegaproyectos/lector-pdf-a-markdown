from pathlib import Path

from pdf_to_md_app.converter import get_pdf_page_count


def test_get_pdf_page_count_reads_sample_pdf() -> None:
    sample_pdf = Path("assets/sample.pdf")
    assert get_pdf_page_count(sample_pdf) == 1
