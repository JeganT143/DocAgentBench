from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class CorpusType(str, Enum):
    PUBMED = "pubmed"
    SEC_10k = "sec_10k"

class IngestResponse(BaseModel):
    document_id: str = Field(description="Unique identifier for the ingested document")
    filename: str = Field(description="Original filename of the ingested document")
    corpus_type: CorpusType = Field(description="Type of the corpus the document belongs to")
    file_size_bytes: int = Field(description="Size of the ingested file in bytes")
    upload_timestamp: datetime = Field(description="Timestamp when the document was ingested")
    storage_path: str = Field(description="Path where the ingested document is stored")

class ErrorResponse(BaseModel):
    error: str = Field(description="Error message describing what went wrong")
    detail: str = Field(description="Detailed information about the error, if available")
    

