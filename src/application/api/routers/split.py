import datetime
import os
import shutil
import json
import uuid
import io
import zipfile
from typing import List, Optional, Union

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from src.application.api.models import ChunkResponse, SplitMethodEnum
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
    split_method: SplitMethodEnum = Form(...),
    metadata: Optional[List[str]] = Form([]),
    split_params: Optional[str] = Form(""),  # Use defaults if empty or "string"
    chunk_path: str = Form("data/output"),
    download_zip: bool = Form(False),  # New parameter: when True, return ZIP instead of JSON
) -> Union[ChunkResponse, StreamingResponse]:
    """
    **Splits the provided document using the specified splitting method.**

    This endpoint handles the file upload, saves the document to the designated path,
    reads and converts the document using `ReadManager`, splits its content using
    `SplitManager`, and saves the resulting chunks using `ChunkManager`.

    **Args:**
    - `file (UploadFile)`: The document file to be split.
    - `document_path (Optional[str])`: The directory path where the document is located.
    - `document_name (Optional[str])`: The name of the document.
    - `document_id (Optional[str])`: A unique identifier for the document.
    - `split_params: Optional[str]`: The parameters for the specific splitting method.
    - `split_method (str)`: The method used to split the document.
    - `metadata (Optional[List[str]])`: Additional metadata for the document.

    **Defaults:**

    - If `document_path` is not provided, it is set to `data/input`.
    - If `document_name` is not provided, it is set to the uploaded file's filename.
    - If `document_id` is not provided, it is set to 
        `{base_filename}_{original_extension}_{date}_{time}` if not provided.
    - If `split_params` are not provided, it is set to specific splitter default params.
    - If `chunk_path`is not provided, it is set to `data/output`.

    **Returns:**
        `ChunkResponse`: A response containing the document chunks and associated metadata.

    **Raises:**
        `HTTPException`: If reading the file or splitting its content fails.
    """

    # Convert file empty string to None.
    if isinstance(file, str) and file.strip() == "":
        file = None

    # Branch based on file upload vs file path.
    if file is not None:
        # === File upload scenario ===
        if not document_path or document_path.lower() == "string":
            document_path = "data/input"
        os.makedirs(document_path, exist_ok=True)

        if not document_name or document_name.strip() == "":
            document_name = file.filename

        document_save_path = os.path.join(document_path, document_name)
        with open(document_save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_dir = document_path
        file_name = document_name
    else:
        # === File path scenario ===
        if not os.path.exists(document_path):
            raise HTTPException(
                status_code=400,
                detail="No file provided and document_path does not exist.",
            )
        file_dir = os.path.dirname(document_path)
        file_name = os.path.basename(document_path)
        if document_name.strip() != "":
            file_name = document_name

    if not document_id or document_id.strip() == "":
        now = datetime.datetime.now()
        date_str = now.strftime("%Y%m%d")
        time_str = now.strftime("%H%M%S")
        uuid_str = uuid.uuid4().hex[:16]
        _, extension = os.path.splitext(file_name)
        document_id = f"{uuid_str}_{date_str}_{time_str}{extension}"

    if not chunk_path or chunk_path.lower() == "string":
        chunk_path = "data/output"
    os.makedirs(chunk_path, exist_ok=True)

    custom_split_params = {}
    if split_params and split_params.lower() != "string":
        try:
            custom_split_params = json.loads(split_params)
            if not isinstance(custom_split_params, dict):
                raise ValueError("split_params must be a JSON object")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid split_params: {str(e)}")

    base_config = {"splitter": {"method": split_method.value}}
    if custom_split_params:
        base_config["splitter"]["methods"] = {split_method.value: custom_split_params}

    read_manager = ReadManager(input_path=file_dir)
    split_manager = SplitManager(config=base_config)
    chunk_manager = ChunkManager(
        input_path=file_dir, output_path=chunk_path, split_method=split_method.value
    )

    try:
        markdown_text = read_manager.read_file(file_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    chunks = split_manager.split_text(markdown_text)
    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks generated from the document.")

    chunk_manager.save_chunks(chunks, file_name, os.path.splitext(file_name)[1], split_method.value)

    chunk_ids = [
        f"{file_name}_{date_str}_{time_str}_chunk_{i}"
        for i in range(1, len(chunks) + 1)
    ]

    # If the user wants to download the output as a ZIP file...
    if download_zip:
        # Create an in-memory ZIP archive.
        zip_io = io.BytesIO()
        with zipfile.ZipFile(zip_io, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            # Add each chunk as a text file.
            for i, chunk in enumerate(chunks, start=1):
                chunk_filename = f"{os.path.splitext(file_name)[0]}_chunk_{i}.txt"
                zip_file.writestr(chunk_filename, chunk)
        zip_io.seek(0)
        headers = {"Content-Disposition": f"attachment; \
                   filename={os.path.splitext(file_name)[0]}_chunks.zip"}
        return StreamingResponse(zip_io, media_type="application/zip", headers=headers)

    # Otherwise, return the standard JSON response.
    return ChunkResponse(
        chunks=chunks,
        chunk_id=chunk_ids,
        chunk_path=chunk_path,
        document_id=document_id,
        document_name=file_name,
        split_method=split_method.value,
        metadata=metadata,
        split_params=custom_split_params,
    )
