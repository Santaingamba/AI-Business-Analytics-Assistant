import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AnalyticsJobBase(BaseModel):
    dataset_id: uuid.UUID
    status: str
    analytics_version: str

class AnalyticsJobResponse(AnalyticsJobBase):
    id: uuid.UUID
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    summary: Optional[Dict[str, Any]] = None
    created_by: Optional[uuid.UUID] = None
    
    model_config = ConfigDict(from_attributes=True)

class KPIResultBase(BaseModel):
    dataset_id: uuid.UUID
    kpi_name: str
    kpi_category: str
    value: Optional[float] = None
    previous_value: Optional[float] = None
    percentage_change: Optional[float] = None
    confidence_score: Optional[float] = None

class KPIResultResponse(KPIResultBase):
    id: uuid.UUID
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

class AnalyticsMetricBase(BaseModel):
    dataset_id: uuid.UUID
    metric_name: str
    metric_category: str
    dimension: Optional[str] = None
    value: Any
    aggregation: Optional[str] = None

class AnalyticsMetricResponse(AnalyticsMetricBase):
    id: uuid.UUID
    generated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class CustomerSegmentBase(BaseModel):
    dataset_id: uuid.UUID
    segment_name: str
    description: Optional[str] = None
    customer_count: int
    revenue: Optional[float] = None
    percentage: Optional[float] = None

class CustomerSegmentResponse(CustomerSegmentBase):
    id: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)

class AnalyticsHistoryBase(BaseModel):
    dataset_id: uuid.UUID
    analytics_type: str
    duration_ms: Optional[int] = None
    version: str
    status: str

class AnalyticsHistoryResponse(AnalyticsHistoryBase):
    id: uuid.UUID
    execution_time: datetime
    
    model_config = ConfigDict(from_attributes=True)
