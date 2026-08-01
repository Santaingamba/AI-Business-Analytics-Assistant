from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any, List, Optional
from app.schemas.ai import AIMessageBase

class BaseLLMClient(ABC):
    """Abstract base class for all LLM providers (Gemini, OpenAI, Claude, etc)."""
    
    @abstractmethod
    async def generate_response(self, system_prompt: str, messages: List[AIMessageBase], **kwargs) -> str:
        """Generate a single string response."""
        pass

    @abstractmethod
    async def generate_stream(self, system_prompt: str, messages: List[AIMessageBase], **kwargs) -> AsyncGenerator[str, None]:
        """Generate a streaming response."""
        pass
        
    @abstractmethod
    async def generate_structured(self, system_prompt: str, user_prompt: str, response_schema: Any, **kwargs) -> Any:
        """Generate a response constrained to a JSON schema (Pydantic model)."""
        pass
