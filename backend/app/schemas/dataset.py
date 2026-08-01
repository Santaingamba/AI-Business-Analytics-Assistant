import uuid
from typing import List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.enums import FileType, ProcessingStatus, Visibility, ColumnDataType

class DatasetColumnBase(BaseModel):
    column_name: str
    detected_data_type: ColumnDataType
    is_nullable: bool
    is_unique: bool = False
    sample_values: Optional[str] = None
    position: int

class DatasetColumnResponse(DatasetColumnBase):
    id: uuid.UUID
    dataset_id: uuid.UUID

    class Config:
        from_attributes = True

class DatasetBase(BaseModel):
    display_name: str
    description: Optional[str] = None
    visibility: Visibility = Visibility.PRIVATE

class DatasetCreate(DatasetBase):
    owner_id: uuid.UUID
    original_filename: str
    stored_filename: str
    file_type: FileType
    file_size_bytes: int
    storage_path: str
    checksum_sha256: str

class DatasetUpdate(BaseModel):
    display_name: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[Visibility] = None
    processing_status: Optional[ProcessingStatus] = None
    encoding: Optional[str] = None
    delimiter: Optional[str] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    deleted_at: Optional[datetime] = None

class DatasetResponse(DatasetBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    original_filename: str
    file_type: FileType
    file_size_bytes: int
    processing_status: ProcessingStatus
    encoding: Optional[str] = None
    delimiter: Optional[str] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DatasetDetailsResponse(DatasetResponse):
    columns: List[DatasetColumnResponse]

class DatasetPreviewResponse(BaseModel):
    headers: List[str]
    data: List[List[Any]]
    row_count: int
    column_count: int
