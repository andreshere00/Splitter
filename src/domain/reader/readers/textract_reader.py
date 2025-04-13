import logging
import os
from typing import Optional

from src.domain.reader.base_reader import (
    BaseReader,
)  # Ensure you have a BaseReader interface


class TextractReader(BaseReader):
    """
    TextractReader extracts text from documents using Amazon Textract's DetectDocumentText API.

    This reader reads the file as bytes, sends it to Textract via the detect_document_text API,
    and then groups the detected text lines by page into a Markdown formatted string.

    Attributes:
        client: A boto3 Textract client instance.
        model (Optional[str]): Not used here, but retained for interface compatibility.
    """

    def __init__(self, client, model: Optional[str] = None):
        self.client = client
        self.model = model

    def convert(self, file_path: str) -> str:
        """
        Converts an input document to Markdown text by extracting text using Textract's
        DetectDocumentText API.

        Args:
            file_path (str): The path to the document file.

        Returns:
            str: A Markdown formatted string with the extracted text, grouped by page.
        """
        # Read the document bytes
        with open(file_path, "rb") as f:
            file_bytes = f.read()

        try:
            # Call Textract's detect_document_text API
            response = self.client.detect_document_text(Document={"Bytes": file_bytes})
        except Exception as e:
            logging.error(f"Textract detect_document_text failed: {e}")
            raise RuntimeError("Textract detect_document_text failed") from e

        # Group detected lines by page. Default page number is 1.
        pages = {}
        for block in response.get("Blocks", []):
            if block.get("BlockType") == "LINE":
                page_num = block.get("Page", 1)
                pages.setdefault(page_num, []).append(block.get("Text", ""))

        # Build Markdown content
        document_name = os.path.basename(file_path)
        markdown_content = f"# Document: {document_name}\n\n"
        if not pages:
            markdown_content += "No text detected."
        else:
            for page in sorted(pages.keys()):
                markdown_content += f"## Page {page}\n\n"
                for line in pages[page]:
                    markdown_content += line + "\n\n"

        return markdown_content
