import uuid
from typing import Optional, Dict, Any, List
from sqlalchemy import Column, String, Float, Integer, Boolean, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, default="PENDING", nullable=False)  # PENDING, RUNNING, COMPLETED, FAILED
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_ms = Column(Integer, nullable=True)
    processing_version = Column(String, nullable=False, default="1.0.0")
    summary = Column(JSON, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    dataset = relationship("Dataset", backref="processing_jobs")

class DatasetStatistics(Base):
    __tablename__ = "dataset_statistics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    row_count = Column(Integer, nullable=False)
    column_count = Column(Integer, nullable=False)
    
    numeric_columns = Column(Integer, default=0)
    categorical_columns = Column(Integer, default=0)
    boolean_columns = Column(Integer, default=0)
    datetime_columns = Column(Integer, default=0)
    text_columns = Column(Integer, default=0)
    
    memory_usage_bytes = Column(Integer, nullable=True)
    null_cells = Column(Integer, default=0)
    duplicate_rows = Column(Integer, default=0)
    duplicate_columns = Column(Integer, default=0)
    
    completeness_score = Column(Float, nullable=True)
    quality_score = Column(Float, nullable=True)

    dataset = relationship("Dataset", backref="statistics")

class ColumnStatistics(Base):
    __tablename__ = "column_statistics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    column_id = Column(UUID(as_uuid=True), ForeignKey("dataset_columns.id", ondelete="CASCADE"), nullable=False)
    
    mean = Column(Float, nullable=True)
    median = Column(Float, nullable=True)
    mode = Column(String, nullable=True)
    variance = Column(Float, nullable=True)
    std_dev = Column(Float, nullable=True)
    min_val = Column(Float, nullable=True)
    max_val = Column(Float, nullable=True)
    range_val = Column(Float, nullable=True)
    q1 = Column(Float, nullable=True)
    q3 = Column(Float, nullable=True)
    iqr = Column(Float, nullable=True)
    
    missing_count = Column(Integer, default=0)
    missing_percentage = Column(Float, default=0.0)
    unique_count = Column(Integer, default=0)
    unique_percentage = Column(Float, default=0.0)
    duplicate_percentage = Column(Float, default=0.0)
    
    outlier_count = Column(Integer, default=0)
    outlier_percentage = Column(Float, default=0.0)
    
    skewness = Column(Float, nullable=True)
    kurtosis = Column(Float, nullable=True)
    entropy = Column(Float, nullable=True)
    
    semantic_type = Column(String, nullable=True)

    column = relationship("DatasetColumn", backref="statistics")

class ProcessingHistory(Base):
    __tablename__ = "processing_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    operation = Column(String, nullable=False)
    parameters = Column(JSON, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    status = Column(String, nullable=False)
    performed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

class TransformationPlan(Base):
    __tablename__ = "transformation_plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    operations = Column(JSON, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
