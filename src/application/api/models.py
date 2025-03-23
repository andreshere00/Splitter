from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class SplitMethodEnum(str, Enum):
    word = "word"
    sentence = "sentence"
    paragraph = "paragraph"
    semantic = "semantic"
    fixed = "fixed"
    paged = "paged"
    recursive = "recursive"
    row_column = "row-column"
    schema_based = "schema-based"
    auto = "auto"


class DocumentRequest(BaseModel):
    """
    Request model for splitting a document.

    Attributes:
        document_name (Optional[str]): The name of the document. If not provided,
            inferred from the uploaded file.
        document_path (str): The path where the document is located.
        document_id (Optional[str]): A unique identifier for the document.
            If not provided, generated automatically.
        split_method (str): The method used for splitting the document.
        split_params (Optional[Dict[str, Any]]): A dictionary of parameters to override the
            default configuration for the splitting method.
        metadata (Optional[List[str]]): Additional metadata for the document.
    """

    document_name: Optional[str] = None
    document_path: str
    document_id: Optional[str] = None
    split_method: str
    split_params: Optional[Dict[str, Any]] = None
    metadata: Optional[List[str]] = []


class ChunkResponse(BaseModel):
    """
    Response model for the document splitting operation.

    Attributes:
        chunks (List[str]): A list of text chunks generated from the document.
        chunk_id (List[str]): Generated IDs for each chunk.
        chunk_path (str): The output path where the chunks are saved.
        document_id (str): The unique identifier for the document.
        document_name (Optional[str]): The name of the document.
        split_method (str): The splitting method used.
        split_params (Optional[Dict[str, Any]]): The custom splitting parameters applied.
        metadata (Optional[List[str]]): Additional metadata for the document.
    """

    chunks: List[str]
    chunk_id: List[str]
    chunk_path: str
    document_id: str
    document_name: Optional[str] = None
    split_method: str
    split_params: Optional[Dict[str, Any]] = None
    metadata: Optional[List[str]] = []
