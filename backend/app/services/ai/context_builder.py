import uuid
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.dataset import Dataset
from app.models.processing import DatasetStatistics, ColumnStatistics
from app.models.analytics import AnalyticsMetric, KPIResult, CustomerSegment

class ContextBuilder:
    """Builds the necessary context from previous data processing and analytics layers."""
    
    def __init__(self, db: Session):
        self.db = db

    def build_dataset_context(self, dataset_id: uuid.UUID) -> Dict[str, Any]:
        dataset = self.db.execute(select(Dataset).filter(Dataset.id == dataset_id)).scalar_one_or_none()
        if not dataset:
            return {}
            
        stats = self.db.execute(select(DatasetStatistics).filter(DatasetStatistics.dataset_id == dataset_id)).scalar_one_or_none()
        
        context = {
            "metadata": {
                "name": dataset.display_name,
                "description": dataset.description,
                "row_count": dataset.row_count,
                "column_count": dataset.column_count
            }
        }
        
        if stats:
            context["statistics"] = {
                "completeness_score": stats.completeness_score,
                "validity_score": stats.validity_score,
                "overall_quality_score": stats.overall_quality_score
            }
            
        # Add column info
        col_stats = self.db.execute(select(ColumnStatistics).filter(ColumnStatistics.dataset_id == dataset_id)).scalars().all()
        context["columns"] = [
            {
                "name": c.column_name,
                "type": c.data_type.value if hasattr(c.data_type, 'value') else c.data_type,
                "null_count": c.null_count,
                "unique_count": c.unique_count
            }
            for c in col_stats
        ]
        
        return context

    def build_analytics_context(self, dataset_id: uuid.UUID) -> Dict[str, Any]:
        metrics = self.db.execute(select(AnalyticsMetric).filter(AnalyticsMetric.dataset_id == dataset_id)).scalars().all()
        kpis = self.db.execute(select(KPIResult).filter(KPIResult.dataset_id == dataset_id)).scalars().all()
        segments = self.db.execute(select(CustomerSegment).filter(CustomerSegment.dataset_id == dataset_id)).scalars().all()
        
        return {
            "metrics": [{"name": m.name, "value": m.value, "category": m.category.value if hasattr(m.category, 'value') else m.category} for m in metrics],
            "kpis": [{"name": k.name, "value": k.value, "trend": k.trend, "target": k.target} for k in kpis],
            "segments": [{"name": s.name, "size": s.size, "description": s.description} for s in segments]
        }

    def build_dashboard_context(self, dashboard_state: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if not dashboard_state:
            return {}
        return {
            "current_view": dashboard_state.get("current_view"),
            "active_filters": dashboard_state.get("filters", []),
            "selected_metrics": dashboard_state.get("metrics", [])
        }
        
    def build_full_context(self, dataset_id: uuid.UUID, dashboard_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {
            "dataset": self.build_dataset_context(dataset_id),
            "analytics": self.build_analytics_context(dataset_id),
            "dashboard": self.build_dashboard_context(dashboard_state)
        }
