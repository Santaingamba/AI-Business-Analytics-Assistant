import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy import Column, String, DateTime, Integer, Float, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base

class AnalyticsJob(Base):
    __tablename__ = "analytics_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), nullable=False, default="PENDING")
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_ms = Column(Integer, nullable=True)
    analytics_version = Column(String(50), nullable=False)
    summary = Column(JSON, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

class KPIResult(Base):
    __tablename__ = "kpi_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    kpi_name = Column(String(100), nullable=False, index=True)
    kpi_category = Column(String(100), nullable=False, index=True)
    value = Column(Float, nullable=True)
    previous_value = Column(Float, nullable=True)
    percentage_change = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    confidence_score = Column(Float, nullable=True)

class AnalyticsMetric(Base):
    __tablename__ = "analytics_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    metric_name = Column(String(100), nullable=False, index=True)
    metric_category = Column(String(100), nullable=False, index=True)
    dimension = Column(String(100), nullable=True)
    value = Column(JSON, nullable=False)
    aggregation = Column(String(50), nullable=True)
    generated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CustomerSegment(Base):
    __tablename__ = "customer_segments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    segment_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    customer_count = Column(Integer, nullable=False)
    revenue = Column(Float, nullable=True)
    percentage = Column(Float, nullable=True)

class AnalyticsHistory(Base):
    __tablename__ = "analytics_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    analytics_type = Column(String(100), nullable=False)
    execution_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    duration_ms = Column(Integer, nullable=True)
    version = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
