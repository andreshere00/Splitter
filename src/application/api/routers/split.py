import datetime
import io
import json
import os
import uuid
import zipfile
from typing import List, Optional, Union

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from src.application.api.models import ChunkResponse, OCRMethodEnum, SplitMethodEnum
from src.chunker.chunk_manager import ChunkManager
from src.reader.read_manager import ReadManager
from src.splitter.split_manager import SplitManager

router = APIRouter()


@router.post(
    "/split",
    response_model=ChunkResponse,
    summary="Split Document",
    description=(
        "Splits a document into chunks using the specified split method. "
        "You can either upload a file or specify a file path. "
        "It has an OCR feature to analyze images from the documents."
        "Optionally, the result can be returned as a ZIP file."
    ),
)
async def split_document(
    file: Optional[Union[UploadFile, str]] = File(
        None, description="Uploaded file. Leave empty if using a file path."
    ),
    document_path: str = Form(
        "data/input",
        description="Absolute or relative path where the document is located.",
    ),
    document_name: str = Form(
        "",
        description="Name for the document; if empty, the uploaded file's name is used.",
    ),
    document_id: str = Form(
        "", description="Optional document identifier. If empty, one will be generated."
    ),
    split_method: SplitMethodEnum = Form(
        ..., description="Method to split the document text."
    ),
    ocr_method: OCRMethodEnum = Form(
        OCRMethodEnum.none,
        description="OCR client to use for image processing: 'none', 'openai', or 'azure'.",
    ),
    metadata: Optional[List[str]] = Form([], description="Optional metadata tags."),
    split_params: str = Form(
        "{}",
        description="JSON string of custom parameters for splitting (must be a JSON object).",
    ),
    chunk_path: str = Form(
        "data/output", description="Path where the output chunks will be stored."
    ),
    download_zip: bool = Form(
        False,
        description="If true, returns the chunks in a ZIP archive instead of JSON.",
    ),
) -> Union[ChunkResponse, StreamingResponse]:
    try:
        # Normalize paths.
        document_path = os.path.abspath(document_path)
        chunk_path = os.path.abspath(chunk_path)

        if isinstance(file, str) and not file.strip():
            file = None

        # Create unique identifiers.
        now = datetime.datetime.now()
        date_str = now.strftime("%Y%m%d")
        time_str = now.strftime("%H%M%S")
        uuid_str = uuid.uuid4().hex[:16]

        # Determine file name and directory.
        if file is not None:
            file_name = document_name.strip() or file.filename
            # Use document_path as base folder for uploads.
            file_dir = document_path
        else:
            if not os.path.exists(document_path):
                raise HTTPException(
                    status_code=400,
                    detail="No file provided and document_path does not exist.",
                )
            file_name = document_name.strip() or os.path.basename(document_path)
            file_dir = os.path.dirname(document_path)

        # Generate document_id if not provided.
        if not document_id.strip():
            document_id = f"{uuid_str}_{date_str}_{time_str}_{file_name}"

        os.makedirs(chunk_path, exist_ok=True)

        # Parse custom split parameters.
        try:
            custom_split_params = json.loads(split_params)
            if not isinstance(custom_split_params, dict):
                raise ValueError("split_params must be a JSON object")
            if not custom_split_params:
                custom_split_params = None
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid split_params: {e}")

        base_config = {"splitter": {"method": split_method.value}}
        if custom_split_params:
            base_config["splitter"]["methods"] = {
                split_method.value: custom_split_params
            }

        # Prepare ReadManager configuration including OCR settings.
        read_config = {
            "file_io": {"input_path": file_dir},
            "ocr": {"method": ocr_method.value},
        }

        # Instantiate managers.
        read_manager = ReadManager(config=read_config)
        split_manager = SplitManager(config=base_config)
        chunk_manager = ChunkManager(
            input_path=file_dir, output_path=chunk_path, split_method=split_method.value
        )

        # Always use ReadManager to process the file.
        markdown_text = (
            read_manager.read_file_object(file)
            if file is not None
            else read_manager.read_file(file_name)
        )

        chunks = split_manager.split_text(markdown_text)
        if not chunks:
            raise HTTPException(
                status_code=400, detail="No chunks generated from the document."
            )

        chunk_manager.save_chunks(
            chunks, file_name, os.path.splitext(file_name)[1], split_method.value
        )

        chunk_ids = [
            f"{file_name}_{date_str}_{time_str}_chunk_{i}"
            for i in range(1, len(chunks) + 1)
        ]

        if download_zip:
            zip_io = io.BytesIO()
            with zipfile.ZipFile(
                zip_io, mode="w", compression=zipfile.ZIP_DEFLATED
            ) as zip_file:
                for i, chunk in enumerate(chunks, start=1):
                    chunk_filename = f"{os.path.splitext(file_name)[0]}_chunk_{i}.txt"
                    zip_file.writestr(chunk_filename, chunk)
            zip_io.seek(0)
            headers = {
                "Content-Disposition": f"attachment; filename={os.path.splitext(file_name)[0]}_chunks.zip"  # noqa: E501
            }
            return StreamingResponse(
                zip_io, media_type="application/zip", headers=headers
            )

        return ChunkResponse(
            chunks=chunks,
            chunk_id=chunk_ids,
            chunk_path=chunk_path,
            document_id=document_id,
            document_name=file_name,
            split_method=split_method.value,
            metadata=metadata,
            split_params=custom_split_params,
            ocr_method=ocr_method,
        )

    except HTTPException as http_exc:
        print("HTTPException encountered:", http_exc.detail)
        raise http_exc
    except Exception as e:
        print("Unhandled error encountered:", e)
        raise HTTPException(status_code=400, detail=f"Unhandled error: {e}")
