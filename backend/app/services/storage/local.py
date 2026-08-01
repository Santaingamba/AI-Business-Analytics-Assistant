import os
import shutil
import aiofiles
from pathlib import Path
from typing import AsyncGenerator
from app.services.storage.base import StorageInterface

class LocalStorageService(StorageInterface):
    def __init__(self, base_dir: str = "storage/uploads"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def save_file(self, file_stream: AsyncGenerator[bytes, None], destination_path: str) -> str:
        full_path = self.base_dir / destination_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(full_path, 'wb') as out_file:
            async for chunk in file_stream:
                await out_file.write(chunk)
                
        return str(destination_path)

    async def delete_file(self, file_path: str) -> bool:
        full_path = self.base_dir / file_path
        if full_path.exists() and full_path.is_file():
            archive_path = self.base_dir / "archive" / file_path
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(full_path), str(archive_path))
            return True
        return False

    async def get_file_stream(self, file_path: str) -> AsyncGenerator[bytes, None]:
        full_path = self.base_dir / file_path
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        async with aiofiles.open(full_path, 'rb') as f:
            while chunk := await f.read(8192):
                yield chunk
                
    def get_absolute_path(self, relative_path: str) -> str:
        return str((self.base_dir / relative_path).absolute())

storage_service = LocalStorageService()
