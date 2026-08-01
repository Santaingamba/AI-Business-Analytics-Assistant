import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.ai import AIConversation, AIMessage
from app.models.enums import AIConversationStatus, MessageRole
from app.schemas.ai import AIMessageBase
import time

class ConversationManager:
    """Manages chat histories, titles, and persistent conversations."""
    
    def __init__(self, db: Session):
        self.db = db
        
    def get_or_create_conversation(self, user_id: uuid.UUID, dataset_id: Optional[uuid.UUID], conversation_id: Optional[uuid.UUID] = None) -> AIConversation:
        if conversation_id:
            conv = self.db.execute(select(AIConversation).filter(AIConversation.id == conversation_id)).scalar_one_or_none()
            if conv:
                return conv
                
        conv = AIConversation(
            user_id=user_id,
            dataset_id=dataset_id,
            title="New AI Chat"
        )
        self.db.add(conv)
        self.db.commit()
        self.db.refresh(conv)
        return conv
        
    def add_message(self, conversation_id: uuid.UUID, role: MessageRole, message: str, tokens: int = 0, response_time: float = 0.0, model: str = "") -> AIMessage:
        msg = AIMessage(
            conversation_id=conversation_id,
            role=role,
            message=message,
            tokens=tokens,
            response_time=response_time,
            model=model
        )
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        
        # Update title based on first message
        if role == MessageRole.USER:
            conv = self.db.execute(select(AIConversation).filter(AIConversation.id == conversation_id)).scalar_one_or_none()
            if conv and conv.title == "New AI Chat":
                conv.title = message[:50] + "..." if len(message) > 50 else message
                self.db.commit()
                
        return msg
        
    def get_history(self, conversation_id: uuid.UUID, limit: int = 10) -> List[AIMessageBase]:
        messages = self.db.execute(
            select(AIMessage)
            .filter(AIMessage.conversation_id == conversation_id)
            .order_by(AIMessage.created_at.desc())
            .limit(limit)
        ).scalars().all()
        
        # Return in chronological order
        return [AIMessageBase(role=m.role, message=m.message) for m in reversed(messages)]
