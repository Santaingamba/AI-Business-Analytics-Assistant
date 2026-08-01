import uuid
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.services.auth import get_current_user
from app.models.user import User
from app.models.enums import AIConversationStatus
from app.schemas.ai import (
    AIChatRequest,
    AIExplainRequest,
    AIRecommendationRequest,
    AISummaryRequest,
    AIConversationResponse,
    AIConversationUpdate
)
from app.services.ai.ai_orchestrator import AIOrchestrator
from app.services.ai.conversation_manager import ConversationManager

router = APIRouter()

@router.post("/chat")
async def chat_with_ai(
    request: AIChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orchestrator = AIOrchestrator(db)
    
    if request.stream:
        # FastAPI StreamingResponse takes a generator
        return StreamingResponse(
            orchestrator.chat_stream(
                user_id=current_user.id,
                message=request.message,
                dataset_id=request.dataset_id,
                conversation_id=request.conversation_id
            ),
            media_type="text/event-stream"
        )
    else:
        # Non-streaming fallback if required
        generator = orchestrator.chat_stream(
            user_id=current_user.id,
            message=request.message,
            dataset_id=request.dataset_id,
            conversation_id=request.conversation_id
        )
        # Consume generator
        result = ""
        async for chunk in generator:
            result += chunk
        return {"response": result}

@router.post("/explain")
async def explain_metric(
    request: AIExplainRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orchestrator = AIOrchestrator(db)
    explanation = await orchestrator.get_explanation(
        dataset_id=request.dataset_id,
        target=request.target,
        dashboard_context=request.context
    )
    return {"explanation": explanation}

@router.get("/conversations", response_model=List[AIConversationResponse])
def get_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    manager = ConversationManager(db)
    from sqlalchemy import select
    from app.models.ai import AIConversation
    
    conversations = db.execute(
        select(AIConversation)
        .filter(AIConversation.user_id == current_user.id)
        .filter(AIConversation.status != AIConversationStatus.ARCHIVED)
        .order_by(AIConversation.updated_at.desc())
    ).scalars().all()
    
    return conversations

@router.get("/conversations/{conversation_id}", response_model=AIConversationResponse)
def get_conversation(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from sqlalchemy import select
    from app.models.ai import AIConversation
    
    conv = db.execute(
        select(AIConversation)
        .filter(AIConversation.id == conversation_id)
        .filter(AIConversation.user_id == current_user.id)
    ).scalar_one_or_none()
    
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    return conv

@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from sqlalchemy import select
    from app.models.ai import AIConversation
    
    conv = db.execute(
        select(AIConversation)
        .filter(AIConversation.id == conversation_id)
        .filter(AIConversation.user_id == current_user.id)
    ).scalar_one_or_none()
    
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    conv.status = AIConversationStatus.ARCHIVED
    db.commit()
    return {"status": "success", "message": "Conversation archived"}

@router.patch("/conversations/{conversation_id}", response_model=AIConversationResponse)
def update_conversation(
    conversation_id: uuid.UUID,
    update_data: AIConversationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from sqlalchemy import select
    from app.models.ai import AIConversation
    
    conv = db.execute(
        select(AIConversation)
        .filter(AIConversation.id == conversation_id)
        .filter(AIConversation.user_id == current_user.id)
    ).scalar_one_or_none()
    
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    if update_data.title is not None:
        conv.title = update_data.title
    if update_data.status is not None:
        conv.status = update_data.status
    if update_data.pinned is not None:
        conv.pinned = update_data.pinned
        
    db.commit()
    db.refresh(conv)
    return conv
