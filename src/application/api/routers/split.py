import datetime
import os
import shutil
import json
import uuid
from typing import List, Optional, Union

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from src.application.api.models import ChunkResponse  # TODO: add Download Chunks endpoint
from src.chunker.chunk_manager import ChunkManager
from src.reader.read_manager import ReadManager
from src.splitter.split_manager import SplitManager

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/split", response_model=ChunkResponse)
async def split_document(
    file: Optional[Union[UploadFile, str]] = File(None),
    document_path: str = Form("data/input"),
    document_name: str = Form(""),  # Allow empty value from UI
    document_id: str = Form(""),    # Allow empty value from UI
    split_method: str = Form(...),
    metadata: Optional[List[str]] = Form([]),
    split_params: Optional[str] = Form(""),  # Use defaults if empty or "string"
    chunk_path: str = Form("data/output"),
):
    # Convert file empty string to None.
    if isinstance(file, str) and file.strip() == "":
        file = None

    # Branch based on file upload vs file path.
    if file is not None:
        # === File upload scenario ===
        # Ensure document_path is treated as a directory.
        if not document_path or document_path.lower() == "string":
            document_path = "data/input"
        os.makedirs(document_path, exist_ok=True)

        # If document_name is empty, default to the file's original filename.
        if not document_name or document_name.strip() == "":
            document_name = file.filename

        # Save the uploaded file.
        document_save_path = os.path.join(document_path, document_name)
        with open(document_save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_dir = document_path
        file_name = document_name
    else:
        # === File path scenario ===
        # Here, document_path is assumed to be the full path to an existing file.
        if not os.path.exists(document_path):
            raise HTTPException(
                status_code=400,
                detail="No file provided and document_path does not exist.",
            )
        # Get directory and filename.
        file_dir = os.path.dirname(document_path)
        file_name = os.path.basename(document_path)
        # If document_name is provided and not empty, override the extracted name.
        if document_name.strip() != "":
            file_name = document_name

    # Generate document_id if not provided or is empty.
    if not document_id or document_id.strip() == "":
        now = datetime.datetime.now()
        date_str = now.strftime("%Y%m%d")
        time_str = now.strftime("%H%M%S")
        uuid_str = uuid.uuid4().hex[:16]  # 16-character UUID.
        _, extension = os.path.splitext(file_name)
        document_id = f"{uuid_str}_{date_str}_{time_str}{extension}"

    # Ensure chunk_path (the output directory) exists.
    if not chunk_path or chunk_path.lower() == "string":
        chunk_path = "data/output"
    os.makedirs(chunk_path, exist_ok=True)

    # Parse custom splitter parameters if provided.
    custom_split_params = {}
    if split_params and split_params.lower() != "string":
        try:
            custom_split_params = json.loads(split_params)
            if not isinstance(custom_split_params, dict):
                raise ValueError("split_params must be a JSON object")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid split_params: {str(e)}")

    # Build configuration for the SplitManager.
    base_config = {"splitter": {"method": split_method}}
    if custom_split_params:
        base_config["splitter"]["methods"] = {split_method: custom_split_params}

    # Instantiate managers using file_dir as the input directory.
    read_manager = ReadManager(input_path=file_dir)
    split_manager = SplitManager(config=base_config)
    chunk_manager = ChunkManager(
        input_path=file_dir, output_path=chunk_path, split_method=split_method
    )

    # Read file content (using file_name).
    try:
        markdown_text = read_manager.read_file(file_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    # Split the text.
    chunks = split_manager.split_text(markdown_text)
    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks generated from the document.")

    # Save the chunks.
    chunk_manager.save_chunks(chunks, file_name, os.path.splitext(file_name)[1], split_method)

    # Generate chunk IDs for each chunk.
    chunk_ids = [
        f"{file_name}_{date_str}_{time_str}_chunk_{i}"
        for i in range(1, len(chunks) + 1)
    ]

    return ChunkResponse(
        chunks=chunks,
        chunk_id=chunk_ids,
        chunk_path=chunk_path,
        document_id=document_id,
        document_name=file_name,
        split_method=split_method,
        metadata=metadata,
        split_params=custom_split_params,
    )
