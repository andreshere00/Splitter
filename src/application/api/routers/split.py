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

    This endpoint handles the file upload, saves the document to the designated path,
    reads and converts the document using `ReadManager`, splits its content using
    `SplitManager`, and saves the resulting chunks using `ChunkManager`.

    Modifications:

    - If `document_path` is not provided or equals "string", it is set to "data/input".
    - If `document_name` is not provided or equals "string", it is set to the uploaded file's
        filename.
    - The `document_id` is generated as `{base_filename}_{original_extension}_{date}_{time}` if
        not provided.
    - The provided `split_method` is used to execute the corresponding splitter.
    - The output path is fixed to "data/output".

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
    # Use "data/input" as the default folder if document_path is not provided or is "string".
    if not document_path or document_path.lower() == "string":
        document_path = "data/input"

    # Ensure the document_path directory exists
    os.makedirs(document_path, exist_ok=True)

    # If document_name is not provided or equals "string", use the basename of file.filename.
    if not document_name or document_name.lower() == "string":
        document_name = file.filename

    # Save the uploaded file to document_path
    document_save_path = os.path.join(document_path, document_name)
    with open(document_save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Generate document_id if not provided
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")
    base_filename, original_extension = os.path.splitext(document_name)
    document_id = (
        document_id  # noqa: W503
        or f"{base_filename}_{original_extension.strip('.')}_{date_str}_{time_str}"  # noqa: W503
    )

    # Use fixed paths: input_path = document_path ("data/input") and output_path = "data/output"
    # If document_path was provided, we ignore it in favor of these defaults for file upload.
    input_path = document_path  # Should be "data/input" by our default logic.
    output_path = "data/output"
    os.makedirs(output_path, exist_ok=True)

    # Instantiate managers using direct parameters:
    read_manager = ReadManager(input_path=input_path)
    split_manager = SplitManager(split_method=split_method)
    chunk_manager = ChunkManager(
        input_path=input_path, output_path=output_path, split_method=split_method
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
        for i in range(1, len(chunks) + 1)  #
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
