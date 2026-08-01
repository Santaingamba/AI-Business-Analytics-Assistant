import uuid
import time
from typing import AsyncGenerator, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.enums import MessageRole
from app.schemas.ai import AIMessageBase
from app.services.ai.context_builder import ContextBuilder
from app.services.ai.conversation_manager import ConversationManager
from app.services.ai.prompt_engine.builder import PromptBuilder
from app.services.ai.prompt_engine.templates import PromptTemplateType
from app.services.ai.llm_provider.base_client import BaseLLMClient
from app.services.ai.llm_provider.gemini_client import GeminiClient
from app.services.ai.token_manager import TokenManager
from app.services.ai.response_validator import ResponseValidator

class AIOrchestrator:
    """Central orchestrator for AI reasoning engine, connecting context, prompt, LLM, and history."""
    
    def __init__(self, db: Session, llm_client: Optional[BaseLLMClient] = None):
        self.db = db
        self.llm_client = llm_client or GeminiClient()
        self.context_builder = ContextBuilder(db)
        self.conversation_manager = ConversationManager(db)
        self.prompt_builder = PromptBuilder()
        
    async def chat_stream(
        self, 
        user_id: uuid.UUID, 
        message: str, 
        dataset_id: Optional[uuid.UUID] = None,
        conversation_id: Optional[uuid.UUID] = None
    ) -> AsyncGenerator[str, None]:
        
        # 1. Setup conversation
        conv = self.conversation_manager.get_or_create_conversation(user_id, dataset_id, conversation_id)
        
        # 2. Add user message
        self.conversation_manager.add_message(conv.id, MessageRole.USER, message)
        
        # 3. Build context
        context = {}
        if dataset_id:
            context = self.context_builder.build_full_context(dataset_id)
            context = TokenManager.prune_context(context)
            
        # 4. Build prompt
        system_prompt = self.prompt_builder.build_prompt(
            PromptTemplateType.GENERAL, 
            context=context,
            question=message
        )
        
        # 5. Fetch history
        history = self.conversation_manager.get_history(conv.id, limit=10)
        
        # 6. Stream from LLM
        start_time = time.time()
        full_response = ""
        
        try:
            async for chunk in self.llm_client.generate_stream(system_prompt, history):
                full_response += chunk
                yield chunk
        except Exception as e:
            fallback = ResponseValidator.fallback_explanation(context, message)
            full_response = f"I encountered an error: {str(e)}. {fallback}"
            yield full_response
            
        # 7. Add AI response to DB
        latency = time.time() - start_time
        tokens = TokenManager.count_tokens(full_response)
        
        self.conversation_manager.add_message(
            conv.id, 
            MessageRole.AI, 
            full_response, 
            tokens=tokens, 
            response_time=latency,
            model=getattr(self.llm_client, "model_name", "unknown")
        )

    async def get_explanation(self, dataset_id: uuid.UUID, target: str, dashboard_context: Optional[Dict] = None) -> str:
        """Explains a specific KPI or metric."""
        context = self.context_builder.build_full_context(dataset_id, dashboard_context)
        context = TokenManager.prune_context(context)
        
        system_prompt = self.prompt_builder.build_prompt(
            PromptTemplateType.KPI_EXPLANATION,
            context=context,
            target=target
        )
        
        try:
            return await self.llm_client.generate_response(system_prompt, [AIMessageBase(role=MessageRole.USER, message=f"Explain {target}")])
        except Exception:
            return ResponseValidator.fallback_explanation(context, target)
