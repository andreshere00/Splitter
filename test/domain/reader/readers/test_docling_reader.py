from unittest.mock import MagicMock, patch

from src.domain.reader.readers.docling_reader import DoclingReader


@patch("src.domain.reader.readers.docling_reader.DocumentConverter")
def test_docling_reader_returns_markdown(mock_converter_class):
    """Test that DoclingReader correctly returns markdown content."""
    # Mock the document conversion response
    mock_document = MagicMock()
    mock_document.export_to_markdown.return_value = "# This is markdown"

    mock_converted_result = MagicMock()
    mock_converted_result.document = mock_document

    mock_converter_instance = MagicMock()
    mock_converter_instance.convert.return_value = mock_converted_result

    mock_converter_class.return_value = mock_converter_instance

    reader = DoclingReader()
    result = reader.convert("fake_path.txt")

    assert result == "# This is markdown"
    mock_converter_instance.convert.assert_called_once_with("fake_path.txt")
    mock_document.export_to_markdown.assert_called_once()
