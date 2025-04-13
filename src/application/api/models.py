from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ReaderMethodEnum(str, Enum):
    """
    Available clients and libraries to read documents.

    Attributes:
        markitdown (str): Uses the MarkItDown tool for Markdown conversion and image description.
        docling (str): Uses the Docling tool to extract structured text and metadata.
        pdfplumber (str): Uses PDFPlumber to extract text and tables from PDF documents.
        textract (str): Uses AWS Textract to extract text from a variety of document formats.
    """

    markitdown = "markitdown"
    docling = "docling"
    pdfplumber = "pdfplumber"
    textract = "textract"


class SplitMethodEnum(str, Enum):
    """
    Available methods to split documents into smaller chunks.

    Attributes:
        word (str): Splits content by a specified number of words.
        sentence (str): Splits content by a specified number of sentences.
        paragraph (str): Splits content by paragraphs.
        fixed (str): Splits content into fixed-size character chunks.
        recursive (str): Uses a recursive strategy for adaptive chunking with overlap.
    """

    word = "word"
    sentence = "sentence"
    paragraph = "paragraph"
    # semantic = "semantic"
    fixed = "fixed"
    # paged = "paged"
    recursive = "recursive"
    # row_column = "row-column"
    # schema_based = "schema-based"
    # auto = "auto"


class OCRMethodEnum(str, Enum):
    """
    Available OCR or VLM methods to analyze and extract text or metadata from images
    and other non-textual content in documents.

    Attributes:
        none (str): No OCR or vision-language model is used.
        openai (str): Uses OpenAI's VLM (e.g., GPT-4 Vision) to analyze image content.
        azure (str): Uses Azure's OpenAI VLM service to analyze image content.
    """

    none = "none"
    openai = "openai"
    azure = "azure"


class DocumentRequest(BaseModel):
    """
    Request model for initiating a document splitting operation.

    Attributes:
        document_name (Optional[str]): The name of the document. If not provided,
            it will be inferred from the file path.
        document_path (str): The absolute or relative path to the input document file.
        document_id (Optional[str]): A unique identifier for the document. If not provided,
            it can be generated internally.
        split_method (SplitMethodEnum): The method used to split the document content.
        split_params (Optional[Dict[str, Any]]): Parameters that override the default
            configuration for the selected split method (e.g., chunk size, overlap).
        metadata (Optional[List[str]]): List of additional metadata tags associated with
            the document.
        reader_method (Optional[str]): The reader backend to use (e.g., "pdfplumber", "markitdown").
    """

    document_name: Optional[str] = None
    document_path: str
    document_id: Optional[str] = None
    split_method: SplitMethodEnum
    split_params: Optional[Dict[str, Any]] = None
    metadata: Optional[List[str]] = []
    reader_method: Optional[str] = "markitdown"


class ChunkResponse(BaseModel):
    """
    Response model returned after successfully splitting a document.

    Attributes:
        chunks (List[str]): The list of extracted text chunks.
        chunk_id (List[str]): The list of unique IDs generated for each chunk.
        chunk_path (str): The directory path where the chunk files are stored.
        document_id (str): The unique identifier assigned to the processed document.
        document_name (Optional[str]): The original name of the document.
        split_method (SplitMethodEnum): The method used to split the document.
        split_params (Optional[Dict[str, Any]]): The parameters applied during splitting.
        metadata (Optional[List[str]]): Any additional metadata associated with the document.
        ocr_method (OCRMethodEnum): The OCR or VLM method used during processing.
        reader_method (Optional[str]): The reader backend used for parsing the document.
    """

    chunks: List[str]
    chunk_id: List[str]
    chunk_path: str
    document_id: str
    document_name: Optional[str] = None
    split_method: SplitMethodEnum
    split_params: Optional[Dict[str, Any]] = None
    metadata: Optional[List[str]] = []
    ocr_method: OCRMethodEnum
    reader_method: Optional[str] = None
