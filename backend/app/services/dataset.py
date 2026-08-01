import uuid
import os
from datetime import datetime, timezone
from typing import AsyncGenerator, Optional, Tuple, List, Any
from sqlalchemy.orm import Session
from fastapi import UploadFile, status

from app.core.exceptions import BaseAppException
from app.models.enums import FileType, ProcessingStatus, Visibility
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetCreate, DatasetUpdate
from app.db.repositories.dataset import dataset_repo, dataset_column_repo
from app.services.storage.local import storage_service
from app.services.file_validator import FileValidatorService
from app.services.schema import SchemaExtractorService
from app.services.preview import PreviewService

class DatasetService:
    @staticmethod
    async def _stream_file(file: UploadFile) -> AsyncGenerator[bytes, None]:
        while chunk := await file.read(8192):
            yield chunk

    @staticmethod
    async def upload_dataset(db: Session, *, user_id: uuid.UUID, file: UploadFile, display_name: str, description: Optional[str] = None, visibility: Visibility = Visibility.PRIVATE) -> Dataset:
        # 1. Validate extension and mime type
        file_type = FileValidatorService.validate_filename_and_type(file.filename, file.content_type)
        
        # 2. Check file size
        if file.size and file.size > FileValidatorService.MAX_FILE_SIZE_BYTES:
            raise BaseAppException("File too large", status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
            
        dataset_id = uuid.uuid4()
        stored_filename = f"{dataset_id}_{file.filename}"
        relative_storage_path = f"{user_id}/{dataset_id}/{file.filename}"
        
        await file.seek(0)
        checksum = await FileValidatorService.generate_checksum_from_stream(DatasetService._stream_file(file))
        
        existing = dataset_repo.get_by_checksum_and_owner(db, checksum=checksum, owner_id=user_id)
        if existing:
            raise BaseAppException("A dataset with this exact content already exists.", status.HTTP_409_CONFLICT)
            
        await file.seek(0)
        
        storage_path = await storage_service.save_file(DatasetService._stream_file(file), relative_storage_path)
        
        abs_path = storage_service.get_absolute_path(storage_path)
        file_size = os.path.getsize(abs_path)
        
        dataset_in = DatasetCreate(
            display_name=display_name or file.filename,
            description=description,
            visibility=visibility,
            owner_id=user_id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            file_type=file_type,
            file_size_bytes=file_size,
            storage_path=storage_path,
            checksum_sha256=checksum
        )
        dataset = dataset_repo.create(db, obj_in=dataset_in)
        
        try:
            if file_type == FileType.CSV:
                columns, row_count = SchemaExtractorService.extract_from_csv(abs_path)
            else:
                columns, row_count = SchemaExtractorService.extract_from_excel(abs_path)
                
            if columns:
                dataset_column_repo.create_multi(db, dataset_id=dataset.id, columns_in=columns)
                
            dataset = dataset_repo.update(db, db_obj=dataset, obj_in=DatasetUpdate(
                processing_status=ProcessingStatus.READY,
                row_count=row_count,
                column_count=len(columns)
            ))
            
        except Exception as e:
            dataset = dataset_repo.update(db, db_obj=dataset, obj_in=DatasetUpdate(
                processing_status=ProcessingStatus.FAILED,
                description=f"Processing failed: {str(e)}"
            ))
            
        return dataset

    @staticmethod
    def delete_dataset(db: Session, *, dataset: Dataset) -> bool:
        dataset_repo.update(db, db_obj=dataset, obj_in=DatasetUpdate(
            deleted_at=datetime.now(timezone.utc)
        ))
        return True

    @staticmethod
    def get_preview(dataset: Dataset, num_rows: int = 20) -> Tuple[List[str], List[List[Any]]]:
        abs_path = storage_service.get_absolute_path(dataset.storage_path)
        return PreviewService.get_preview(abs_path, dataset.file_type, num_rows)
