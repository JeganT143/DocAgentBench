import uuid 
import aiofiles
from pathlib import Path
from datetime import datetime, timezone

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse

from models.documents import IngestResponse, ErrorResponse, CorpusType

router = APIRouter(prefix="/ingest", tags=["Document Ingestion"])

UPLOAD_DIR = Path("/app/data/uploads")
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".tiff"}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

@router.post("/", responses={
    400: {"model": ErrorResponse, "description": "Bad Request - Invalid file or parameters"},
    413: {"model": ErrorResponse, "description": "Payload Too Large - File exceeds size limit"},
    500: {"model": ErrorResponse, "description": "Internal Server Error - Something went wrong during file processing"}
    },
    summary="Upload a document for ingestion",
    description="Accepts a PDF or image file and store it for OCR processing"
    )
async def ingest_document(
    file: UploadFile = File(description="The document file to upload"),
    corpus_type: CorpusType = Form(description="The type of corpus the document belongs to")
):
    """
    Receives a document upload, validates it, and saves it to disk.
    Returns metadata about the stored document.
    """

    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_extension}. Allowed types are: {', '.join(ALLOWED_EXTENSIONS)}")
    file_bytes = await file.read()
    file_size = len(file_bytes)
    if file_size == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File size exceeds the maximum allowed limit of {MAX_FILE_SIZE / (1024 * 1024)} MB")
    
    document_id = str(uuid.uuid4())
    corpus_dir = UPLOAD_DIR / corpus_type.value
    corpus_dir.mkdir(parents=True, exist_ok=True)
    safe_filename = f"{document_id}_{Path(file.filename).stem}{file_extension}"
    storage_path = corpus_dir / safe_filename

    try:
        async with aiofiles.open(storage_path, 'wb') as f:
            await f.write(file_bytes)
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to save the file: {str(e)}")
    
    return IngestResponse(
        document_id=document_id,
        filename=file.filename,
        corpus_type=corpus_type,
        file_size_bytes=file_size,
        upload_timestamp=datetime.now(timezone.utc),
        storage_path=str(storage_path)
    )

@router.get("/health", summary="Check ingestion service health")
async def check_health():
    upload_dir_exists = UPLOAD_DIR.exists() and UPLOAD_DIR.is_dir()
    return {
        "status": "healthy" if upload_dir_exists else "unhealthy",
        "upload_directory": str(UPLOAD_DIR),
        "Upload_dir_accessible": upload_dir_exists
    }