import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ProcessingJobBase(BaseModel):
    dataset_id: uuid.UUID
    status: str
    processing_version: str

class ProcessingJobCreate(ProcessingJobBase):
    pass

class ProcessingJobResponse(ProcessingJobBase):
    id: uuid.UUID
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    summary: Optional[Dict[str, Any]] = None
    
    model_config = ConfigDict(from_attributes=True)

class DatasetStatisticsBase(BaseModel):
    dataset_id: uuid.UUID
    row_count: int
    column_count: int
    numeric_columns: int = 0
    categorical_columns: int = 0
    boolean_columns: int = 0
    datetime_columns: int = 0
    text_columns: int = 0
    memory_usage_bytes: Optional[int] = None
    null_cells: int = 0
    duplicate_rows: int = 0
    duplicate_columns: int = 0
    completeness_score: Optional[float] = None
    quality_score: Optional[float] = None

class DatasetStatisticsCreate(DatasetStatisticsBase):
    pass

class DatasetStatisticsResponse(DatasetStatisticsBase):
    id: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)

class ColumnStatisticsBase(BaseModel):
    dataset_id: uuid.UUID
    column_id: uuid.UUID
    mean: Optional[float] = None
    median: Optional[float] = None
    mode: Optional[str] = None
    variance: Optional[float] = None
    std_dev: Optional[float] = None
    min_val: Optional[float] = None
    max_val: Optional[float] = None
    range_val: Optional[float] = None
    q1: Optional[float] = None
    q3: Optional[float] = None
    iqr: Optional[float] = None
    missing_count: int = 0
    missing_percentage: float = 0.0
    unique_count: int = 0
    unique_percentage: float = 0.0
    duplicate_percentage: float = 0.0
    outlier_count: int = 0
    outlier_percentage: float = 0.0
    skewness: Optional[float] = None
    kurtosis: Optional[float] = None
    entropy: Optional[float] = None
    semantic_type: Optional[str] = None

class ColumnStatisticsCreate(ColumnStatisticsBase):
    pass

class ColumnStatisticsResponse(ColumnStatisticsBase):
    id: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)
    
class TransformationPlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    operations: List[Dict[str, Any]]

class TransformationPlanCreate(TransformationPlanBase):
    dataset_id: uuid.UUID

class TransformationPlanResponse(TransformationPlanBase):
    id: uuid.UUID
    dataset_id: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)
