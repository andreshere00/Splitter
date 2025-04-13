from unittest.mock import MagicMock, patch

import pytest

from src.domain.reader.readers.pdfplumber_reader import PDFPlumberReader


@pytest.fixture
def dummy_pdf_page():
    page = MagicMock()
    page.page_number = 1
    page.extract_text_lines.return_value = [
        {"text": "Hello, World!", "top": 100},
        {"text": "Another line", "top": 120},
    ]
    page.lines = []
    page.rects = []
    page.curves = []

    dummy_table = MagicMock()
    dummy_table.extract.return_value = [["Header1", "Header2"], ["Cell1", "Cell2"]]
    dummy_table.bbox = [0, 0, 100, 100]
    page.find_tables.return_value = [dummy_table]
    return page


@patch("src.domain.reader.readers.pdfplumber_reader.pdfplumber.open")
def test_pdfplumber_reader_converts_pdf_to_markdown(mock_pdf_open, dummy_pdf_page):
    """Test that PDFPlumberReader extracts text and tables into Markdown format."""
    mock_pdf = MagicMock()
    mock_pdf.pages = [dummy_pdf_page]
    mock_pdf_open.return_value.__enter__.return_value = mock_pdf

    reader = PDFPlumberReader()
    result = reader.convert("fake_path.pdf")

    assert "# Document: fake_path.pdf" in result
    assert "## Page 1" in result
    assert "Hello, World!" in result
    assert "Another line" in result
    assert "| Header1 | Header2 |" in result
    assert "| Cell1 | Cell2 |" in result


@patch("src.domain.reader.readers.pdfplumber_reader.pdfplumber.open")
def test_pdfplumber_reader_handles_empty_tables(mock_pdf_open):
    """Test that PDFPlumberReader handles tables with failed extraction gracefully."""
    page = MagicMock()
    page.page_number = 1
    page.extract_text_lines.return_value = []
    page.lines = []
    page.rects = []
    page.curves = []

    # Simulate a table extraction error
    table = MagicMock()
    table.extract.side_effect = Exception("Extraction failed")
    table.bbox = [0, 0, 100, 100]
    page.find_tables.return_value = [table]

    mock_pdf = MagicMock()
    mock_pdf.pages = [page]
    mock_pdf_open.return_value.__enter__.return_value = mock_pdf

    reader = PDFPlumberReader()
    markdown = reader.convert("somefile.pdf")

    assert "## Page 1" in markdown
    assert "Document: somefile.pdf" in markdown  # Still processes the document
