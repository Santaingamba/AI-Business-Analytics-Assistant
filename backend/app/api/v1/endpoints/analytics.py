import uuid
from typing import List, Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.api.dependencies.database import get_db
from app.models.user import User
from app.api.dependencies.auth import get_current_active_user as get_current_user
from app.models.analytics import AnalyticsJob, KPIResult, AnalyticsMetric, CustomerSegment
from app.schemas.analytics import AnalyticsJobResponse, KPIResultResponse, AnalyticsMetricResponse, CustomerSegmentResponse
from app.services.analytics.orchestrator import AnalyticsOrchestrator

router = APIRouter()

@router.post("/{dataset_id}/analyze", response_model=AnalyticsJobResponse)
def run_analytics(
    dataset_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orchestrator = AnalyticsOrchestrator(db)
    try:
        job = orchestrator.start_analytics_job(dataset_id=dataset_id, user_id=current_user.id)
        # We need a new session for background tasks ideally, but passing the id and making orchestrator create a session
        # is better. For this version, let's keep it simple with existing orchestrator logic.
        background_tasks.add_task(orchestrator.run_pipeline, job.id)
        return job
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{dataset_id}/status", response_model=AnalyticsJobResponse)
def get_analytics_status(
    dataset_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = db.query(AnalyticsJob).filter(
        AnalyticsJob.dataset_id == dataset_id
    ).order_by(AnalyticsJob.started_at.desc()).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="No analytics job found for this dataset")
    return job

@router.get("/{dataset_id}/kpis", response_model=List[KPIResultResponse])
def get_kpis(
    dataset_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    kpis = db.query(KPIResult).filter(KPIResult.dataset_id == dataset_id).all()
    return kpis

@router.get("/{dataset_id}/metrics", response_model=List[AnalyticsMetricResponse])
def get_metrics(
    dataset_id: uuid.UUID,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(AnalyticsMetric).filter(AnalyticsMetric.dataset_id == dataset_id)
    if category:
        query = query.filter(AnalyticsMetric.metric_category == category)
    return query.all()

@router.get("/{dataset_id}/segments", response_model=List[CustomerSegmentResponse])
def get_segments(
    dataset_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    segments = db.query(CustomerSegment).filter(CustomerSegment.dataset_id == dataset_id).all()
    return segments
