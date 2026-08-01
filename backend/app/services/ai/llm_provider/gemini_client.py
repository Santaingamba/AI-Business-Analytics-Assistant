import os
import google.generativeai as genai
from typing import AsyncGenerator, Dict, Any, List, Optional
from app.services.ai.llm_provider.base_client import BaseLLMClient
from app.schemas.ai import AIMessageBase
from app.models.enums import MessageRole
import logging

logger = logging.getLogger(__name__)

class GeminiClient(BaseLLMClient):
    def __init__(self, model_name: str = "gemini-1.5-pro"):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY environment variable is missing. LLM calls will fail.")
        else:
            genai.configure(api_key=api_key)
        self.model_name = model_name
        
    def _format_messages(self, messages: List[AIMessageBase]) -> List[Dict[str, Any]]:
        formatted = []
        for msg in messages:
            # Gemini expects 'user' or 'model'
            role = "user" if msg.role == MessageRole.USER else "model"
            formatted.append({"role": role, "parts": [msg.message]})
        return formatted

    async def generate_response(self, system_prompt: str, messages: List[AIMessageBase], **kwargs) -> str:
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_prompt
        )
        
        if not messages:
            return ""
            
        history = self._format_messages(messages[:-1])
        chat = model.start_chat(history=history)
        response = await chat.send_message_async(messages[-1].message)
        return response.text

    async def generate_stream(self, system_prompt: str, messages: List[AIMessageBase], **kwargs) -> AsyncGenerator[str, None]:
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_prompt
        )
        
        if not messages:
            return
            
        history = self._format_messages(messages[:-1])
        chat = model.start_chat(history=history)
        response = await chat.send_message_async(messages[-1].message, stream=True)
        
        async for chunk in response:
            if chunk.text:
                yield chunk.text

    async def generate_structured(self, system_prompt: str, user_prompt: str, response_schema: Any, **kwargs) -> Any:
        # Pydantic schema to Gemini schema might require version specific mapping. 
        # Using simple JSON response mime type for broader compatibility.
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_prompt + "\n\nYou MUST return a valid JSON object matching the requested schema. Do not include markdown code blocks.",
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        response = await model.generate_content_async(user_prompt)
        return response_schema.model_validate_json(response.text)
