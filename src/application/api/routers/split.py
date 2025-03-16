import datetime
import os
import shutil
from typing import List, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from src.application.api.models import ChunkResponse
from src.chunker.chunk_manager import ChunkManager
from src.reader.read_manager import ReadManager
from src.splitter.split_manager import SplitManager

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/split", response_model=ChunkResponse)
async def split_document(
    file: UploadFile = File(...),
    document_path: Optional[str] = Form(None),
    document_name: Optional[str] = Form(None),
    document_id: Optional[str] = Form(None),
    split_method: Optional[str] = Form(...),
    metadata: Optional[List[str]] = Form([]),
):
    """
    Splits the provided document using the specified splitting method.

    This endpoint handles the file upload, saves the document to the given path,
    reads and converts the document using `ReadManager`, splits its content using
    `SplitManager`, and saves the resulting chunks using `ChunkManager`.

    The following modifications are applied:

    - If `document_path` is not provided, it is set to the current working directory.
    - If `document_name` is not provided or equals the default placeholder ("string"),
      it is inferred from the uploaded file's filename.
    - The `document_id` is generated as `{base_filename}_{original_extension}_{date}_{time}`
        if not provided.
    - The provided `split_method` is used to execute the corresponding splitter.

    Args:
        file (UploadFile): The document file to be split.
        document_path (Optional[str]): The directory path where the document is located.
        document_name (Optional[str]): The name of the document.
        document_id (Optional[str]): A unique identifier for the document.
        split_method (Optional[str]): The method used to split the document.
        metadata (Optional[List[str]]): Additional metadata for the document.

    Returns:
        ChunkResponse: A response containing the document chunks and associated metadata.

    Raises:
        HTTPException: If reading the file or splitting its content fails.
    """
    # Set document_path to current directory if not provided
    if not document_path:
        document_path = os.getcwd()

    # Ensure the document_path directory exists
    os.makedirs(document_path, exist_ok=True)

    # Infer document name if not provided or if it equals the placeholder "string"
    if not document_name or document_name.lower() == "string":
        document_name = file.filename

    # Save the uploaded file
    document_save_path = os.path.join(document_path, document_name)
    with open(document_save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Generate document_id if not provided
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")
    base_filename, original_extension = os.path.splitext(document_name)
    document_id = (
        document_id
        or f"{base_filename}_{original_extension.strip('.')}_{date_str}_{time_str}"  # noqa: W503
    )

    # Instantiate managers using direct parameters instead of a config file:
    # ReadManager: pass input_path
    read_manager = ReadManager(input_path=document_path)
    # SplitManager: pass the split_method
    split_manager = SplitManager(split_method=split_method)
    # ChunkManager: pass input_path and output_path (defaults to <input_path>/output)
    output_path = os.path.join(document_path, "output")
    chunk_manager = ChunkManager(
        input_path=document_path, output_path=output_path, split_method=split_method
    )

    # Read file content
    try:
        markdown_text = read_manager.read_file(document_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    # Split the text content using the specified split_method
    chunks = split_manager.split_text(markdown_text)
    if not chunks:
        raise HTTPException(
            status_code=400, detail="No chunks generated from the document."
        )

    # Save the chunks
    chunk_manager.save_chunks(chunks, base_filename, original_extension, split_method)

    # Generate chunk IDs for each chunk
    chunk_ids = [
        f"{base_filename}_{original_extension.strip('.')}_{date_str}_{time_str}_chunk_{i}"
        for i in range(1, len(chunks) + 1)
    ]

    return ChunkResponse(
        chunks=chunks,
        chunk_id=chunk_ids,
        chunk_path=output_path,
        document_id=document_id,
        document_name=document_name,
        split_method=split_method,
        metadata=metadata,
    )
