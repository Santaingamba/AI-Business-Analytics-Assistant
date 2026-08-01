import hashlib
import os
from typing import AsyncGenerator
from fastapi import UploadFile, status
from app.core.exceptions import BaseAppException
from app.models.enums import FileType

class FileValidatorService:
    ALLOWED_EXTENSIONS = {
        "csv": FileType.CSV,
        "xlsx": FileType.EXCEL,
        "xls": FileType.EXCEL,
    }
    
    ALLOWED_MIME_TYPES = {
        "text/csv": FileType.CSV,
        "application/vnd.ms-excel": FileType.EXCEL,
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": FileType.EXCEL,
    }
    
    MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024  # 100MB for Phase 2A
    
    @classmethod
    def validate_filename_and_type(cls, filename: str, content_type: str) -> FileType:
        if not filename:
            raise BaseAppException("Filename is missing", status.HTTP_400_BAD_REQUEST)
            
        ext = filename.split('.')[-1].lower() if '.' in filename else ''
        if ext not in cls.ALLOWED_EXTENSIONS:
            raise BaseAppException(
                f"File extension '.{ext}' is not supported. Supported extensions: {', '.join(cls.ALLOWED_EXTENSIONS.keys())}",
                status.HTTP_400_BAD_REQUEST
            )
            
        return cls.ALLOWED_EXTENSIONS[ext]
        
    @classmethod
    async def generate_checksum_from_stream(cls, file_stream: AsyncGenerator[bytes, None]) -> str:
        sha256_hash = hashlib.sha256()
        async for chunk in file_stream:
            sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
