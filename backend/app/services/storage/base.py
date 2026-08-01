from abc import ABC, abstractmethod
from typing import AsyncGenerator

class StorageInterface(ABC):
    @abstractmethod
    async def save_file(self, file_stream: AsyncGenerator[bytes, None], destination_path: str) -> str:
        pass

    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        pass

    @abstractmethod
    async def get_file_stream(self, file_path: str) -> AsyncGenerator[bytes, None]:
        pass
        
    @abstractmethod
    def get_absolute_path(self, relative_path: str) -> str:
        pass
