import uuid
import pandas as pd
import time
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.dataset import Dataset
from app.models.analytics import AnalyticsJob, KPIResult, AnalyticsMetric, CustomerSegment, AnalyticsHistory
from app.core.config import settings

from .inference_engine import InferenceEngine
from .kpi_engine import KPIEngine
from .revenue_analytics import RevenueAnalytics
from .customer_analytics import CustomerAnalytics
from .product_analytics import ProductAnalytics
from .sales_analytics import SalesAnalytics
from .time_series import TimeSeriesAnalytics
from .cohort import CohortAnalytics
from .segmentation import SegmentationEngine
from .trend_analyzer import TrendAnalyzer
from .benchmark import BenchmarkEngine
from .forecast_prep import ForecastPreparation

class AnalyticsOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        
    def start_analytics_job(self, dataset_id: uuid.UUID, user_id: uuid.UUID = None) -> AnalyticsJob:
        job = AnalyticsJob(
            dataset_id=dataset_id,
            status="PROCESSING",
            analytics_version="1.0.0",
            created_by=user_id,
            started_at=datetime.now(timezone.utc)
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def run_pipeline(self, job_id: uuid.UUID):
        job = self.db.query(AnalyticsJob).filter(AnalyticsJob.id == job_id).first()
        if not job:
            return
            
        start_time = time.time()
        
        try:
            dataset = self.db.query(Dataset).filter(Dataset.id == job.dataset_id).first()
            if not dataset:
                raise ValueError("Dataset not found")
                
            file_path = f"{settings.STORAGE_DIR}/{dataset.id}.{dataset.file_type.value}"
            if dataset.file_type.value == 'csv':
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
                
            self.db.query(KPIResult).filter(KPIResult.dataset_id == dataset.id).delete()
            self.db.query(AnalyticsMetric).filter(AnalyticsMetric.dataset_id == dataset.id).delete()
            self.db.query(CustomerSegment).filter(CustomerSegment.dataset_id == dataset.id).delete()
                
            roles = InferenceEngine.infer_roles(df)
            
            kpis = KPIEngine.calculate_kpis(df, roles)
            for kpi in kpis:
                self.db.add(KPIResult(dataset_id=dataset.id, **kpi))
                
            engines = [
                RevenueAnalytics,
                CustomerAnalytics,
                ProductAnalytics,
                SalesAnalytics,
                TimeSeriesAnalytics,
                CohortAnalytics,
                TrendAnalyzer,
                BenchmarkEngine,
                ForecastPreparation
            ]
            
            for engine in engines:
                metrics = engine.analyze(df, roles)
                for metric in metrics:
                    self.db.add(AnalyticsMetric(dataset_id=dataset.id, **metric))
                    
            segments = SegmentationEngine.analyze(df, roles)
            for seg in segments:
                self.db.add(CustomerSegment(dataset_id=dataset.id, **seg))
                
            self.db.commit()
            
            job.status = "COMPLETED"
            job.completed_at = datetime.now(timezone.utc)
            job.duration_ms = int((time.time() - start_time) * 1000)
            job.summary = {"inferred_roles": roles}
            
            history = AnalyticsHistory(
                dataset_id=dataset.id,
                analytics_type="FULL_PIPELINE",
                duration_ms=job.duration_ms,
                version="1.0.0",
                status="SUCCESS"
            )
            self.db.add(history)
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            job.status = "FAILED"
            job.summary = {"error": str(e)}
            job.completed_at = datetime.now(timezone.utc)
            job.duration_ms = int((time.time() - start_time) * 1000)
            self.db.commit()
