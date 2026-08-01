from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, Any
from datetime import datetime, timezone

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    metadata: Optional[dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
