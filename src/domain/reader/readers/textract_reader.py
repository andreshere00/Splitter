from typing import Union
from src.domain.reader.base_reader import BaseReader
from src.infrastructure.model.models.textract_client import TextractClient


class TextractReader(BaseReader):
    """
    Reader that extracts text from images using AWS Textract.
    
    It supports two modes:
      - 'detect': Uses detect_document_text to extract text.
      - 'analyze': Uses analyze_document to extract text after analyzing 
        the document.
    """

    def __init__(self, textract_client: TextractClient, mode: str = "detect"):
        """
        Initialize the TextractReader.

        :param textract_client: An instance of TextractClient.
        :param mode: Extraction mode. Must be either 'detect' or 'analyze'.
        """
        mode = mode.lower()
        if mode not in ("detect", "analyze"):
            raise ValueError("mode must be either 'detect' or 'analyze'")
        self.textract_client = textract_client
        self.mode = mode

    def convert(self, file_path: str) -> Union[str, dict]:
        """
        Extracts text from an image file using the specified Textract method.

        :param file_path: Path to the image file.
        :return: Extracted text as a string.
        """
        # Read the image file as binary
        with open(file_path, "rb") as f:
            image_bytes = f.read()

        client = self.textract_client.get_client()

        if self.mode == "detect":
            response = client.detect_document_text(Document={"Bytes": image_bytes})
        elif self.mode == "analyze":
            # For analyze_document, we provide feature types (e.g., TABLES and FORMS).
            response = client.analyze_document(
                Document={"Bytes": image_bytes},
                FeatureTypes=["TABLES", "FORMS"]
            )
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

        # Process the Textract response: extract text from blocks of type "LINE"
        lines = [
            block.get("Text", "")
            for block in response.get("Blocks", [])
            if block.get("BlockType") == "LINE" and "Text" in block
        ]
        return "\n".join(lines)
