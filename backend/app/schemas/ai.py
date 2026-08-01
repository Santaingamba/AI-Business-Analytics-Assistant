from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Any, Dict
from datetime import datetime
from app.models.enums import AIConversationStatus, MessageRole, InsightCategory, ImportanceLevel, RecommendationStatus

# Message Schemas
class AIMessageBase(BaseModel):
    role: MessageRole
    message: str

class AIMessageCreate(AIMessageBase):
    tokens: Optional[int] = None
    response_time: Optional[float] = None
    model: Optional[str] = None

class AIMessageResponse(AIMessageBase):
    id: UUID4
    conversation_id: UUID4
    created_at: datetime
    
    class Config:
        from_attributes = True

# Conversation Schemas
class AIConversationBase(BaseModel):
    title: str

class AIConversationCreate(AIConversationBase):
    dataset_id: Optional[UUID4] = None

class AIConversationUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[AIConversationStatus] = None
    pinned: Optional[bool] = None

class AIConversationResponse(AIConversationBase):
    id: UUID4
    user_id: UUID4
    dataset_id: Optional[UUID4]
    status: AIConversationStatus
    pinned: bool
    created_at: datetime
    updated_at: datetime
    messages: List[AIMessageResponse] = []
    
    class Config:
        from_attributes = True

class AIConversationListResponse(AIConversationBase):
    id: UUID4
    dataset_id: Optional[UUID4]
    status: AIConversationStatus
    pinned: bool
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Request Schemas for the API Endpoints
class AIChatRequest(BaseModel):
    message: str
    dataset_id: Optional[UUID4] = None
    conversation_id: Optional[UUID4] = None
    stream: bool = False

class AIExplainRequest(BaseModel):
    dataset_id: UUID4
    target: str = Field(..., description="The chart, KPI, or metric to explain")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context from dashboard")

class AIRecommendationRequest(BaseModel):
    dataset_id: UUID4

class AISummaryRequest(BaseModel):
    dataset_id: UUID4
    dashboard_state: Optional[Dict[str, Any]] = None

# Insight and Recommendation Response Schemas
class AIInsightResponse(BaseModel):
    id: UUID4
    dataset_id: UUID4
    category: InsightCategory
    insight: str
    confidence: float
    importance: ImportanceLevel
    source: Optional[str]
    generated_at: datetime

    class Config:
        from_attributes = True

class AIRecommendationResponse(BaseModel):
    id: UUID4
    dataset_id: UUID4
    priority: ImportanceLevel
    recommendation: str
    business_impact: Optional[str]
    confidence: float
    status: RecommendationStatus
    created_at: datetime

    class Config:
        from_attributes = True
