import datetime
import io
import json
import os
import shutil
import uuid
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
    document_id: str = Form(""),  # Allow empty value from UI
    split_method: SplitMethodEnum = Form(...),
    metadata: Optional[List[str]] = Form([]),
    split_params: str = Form("{}"),
    chunk_path: str = Form("data/output"),
    download_zip: bool = Form(False),  # When True, return ZIP instead of JSON
) -> Union[ChunkResponse, StreamingResponse]:
    try:
        # Convert provided paths to absolute paths
        document_path = os.path.abspath(document_path)
        chunk_path = os.path.abspath(chunk_path)

        # Convert file empty string to None.
        if isinstance(file, str) and file.strip() == "":
            file = None

        now = datetime.datetime.now()
        date_str = now.strftime("%Y%m%d")
        time_str = now.strftime("%H%M%S")
        uuid_str = uuid.uuid4().hex[:16]

        # Branch based on file upload vs file path.
        if file is not None:
            # Ensure document_path is treated as a directory.
            if not document_path or document_path.lower() == "string":
                document_path = os.path.abspath("data/input")
            os.makedirs(document_path, exist_ok=True)
            if not document_name or document_name.strip() == "":
                document_name = file.filename
            document_save_path = os.path.join(document_path, document_name)
            with open(document_save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_dir = document_path
            file_name = document_name
        else:
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
            raise HTTPException(
                status_code=400, detail=f"Invalid split_params: {str(e)}"
            )

        base_config = {"splitter": {"method": split_method.value}}
        if custom_split_params:
            base_config["splitter"]["methods"] = {
                split_method.value: custom_split_params
            }

        # Instantiate managers using the absolute paths.
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
                "Content-Disposition": f"attachment; \
                    filename={os.path.splitext(file_name)[0]}_chunks.zip"
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
        )
    except HTTPException as http_exc:
        print("HTTPException encountered:", http_exc.detail)
        raise http_exc
    except Exception as e:
        # Print the error to the console and return a 400 error with the exact error message.
        print("Unhandled error encountered:", e)
        raise HTTPException(status_code=400, detail=f"Unhandled error: {str(e)}")
