import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Boolean, DateTime, Enum as SQLEnum, Integer, ForeignKey, Float, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.enums import AIConversationStatus, MessageRole, InsightCategory, ImportanceLevel, RecommendationStatus

class AIConversation(Base):
    __tablename__ = "ai_conversations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=False)
    dataset_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("datasets.id"), index=True, nullable=True)
    
    title: Mapped[str] = mapped_column(String(200), nullable=False, default="New Conversation")
    status: Mapped[AIConversationStatus] = mapped_column(SQLEnum(AIConversationStatus), default=AIConversationStatus.ACTIVE, nullable=False)
    pinned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    messages: Mapped[List["AIMessage"]] = relationship("AIMessage", back_populates="conversation", cascade="all, delete-orphan", order_by="AIMessage.created_at")
    user = relationship("User")
    dataset = relationship("Dataset")

class AIMessage(Base):
    __tablename__ = "ai_messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    conversation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_conversations.id"), index=True, nullable=False)
    
    role: Mapped[MessageRole] = mapped_column(SQLEnum(MessageRole), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    tokens: Mapped[int] = mapped_column(Integer, nullable=True)
    response_time: Mapped[float] = mapped_column(Float, nullable=True) # in seconds
    model: Mapped[str] = mapped_column(String(100), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    conversation: Mapped["AIConversation"] = relationship("AIConversation", back_populates="messages")

class AIInsight(Base):
    __tablename__ = "ai_insights"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("datasets.id"), index=True, nullable=False)
    
    category: Mapped[InsightCategory] = mapped_column(SQLEnum(InsightCategory), nullable=False)
    insight: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    importance: Mapped[ImportanceLevel] = mapped_column(SQLEnum(ImportanceLevel), nullable=False)
    source: Mapped[str] = mapped_column(String(200), nullable=True) # e.g. "Prompt Hash", "Analytics Layer"
    
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    dataset = relationship("Dataset")

class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("datasets.id"), index=True, nullable=False)
    
    priority: Mapped[ImportanceLevel] = mapped_column(SQLEnum(ImportanceLevel), nullable=False)
    recommendation: Mapped[str] = mapped_column(Text, nullable=False)
    business_impact: Mapped[str] = mapped_column(Text, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[RecommendationStatus] = mapped_column(SQLEnum(RecommendationStatus), default=RecommendationStatus.NEW, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    dataset = relationship("Dataset")

class AIAudit(Base):
    __tablename__ = "ai_audits"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    conversation_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("ai_conversations.id"), index=True, nullable=True)
    
    prompt_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    token_usage: Mapped[int] = mapped_column(Integer, nullable=False)
    latency: Mapped[float] = mapped_column(Float, nullable=False) # response time in ms
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    errors: Mapped[str] = mapped_column(Text, nullable=True)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    conversation = relationship("AIConversation")
