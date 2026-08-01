import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.dependencies.auth import get_current_active_user
from app.models.user import User
from app.models.dataset import Dataset
from app.models.processing import ProcessingJob, DatasetStatistics, ColumnStatistics
from app.schemas.processing import ProcessingJobResponse, DatasetStatisticsResponse, ColumnStatisticsResponse
from app.services.processing.orchestrator import ProcessingOrchestrator

router = APIRouter()

@router.post("/{dataset_id}/profile", response_model=ProcessingJobResponse)
def trigger_profiling(
    dataset_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id, Dataset.owner_id == current_user.id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    orchestrator = ProcessingOrchestrator(db)
    
    existing = db.query(ProcessingJob).filter(
        ProcessingJob.dataset_id == dataset_id, 
        ProcessingJob.status.in_(["PENDING", "RUNNING"])
    ).first()
    
    if existing:
        return existing
        
    job = orchestrator.create_job(dataset_id=dataset_id, user_id=current_user.id)
    background_tasks.add_task(orchestrator.run_profiling, job.id)
    
    return job

@router.get("/{dataset_id}/profile/status", response_model=ProcessingJobResponse)
def get_profiling_status(
    dataset_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id, Dataset.owner_id == current_user.id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    job = db.query(ProcessingJob).filter(ProcessingJob.dataset_id == dataset.id).order_by(ProcessingJob.started_at.desc()).first()
    if not job:
        raise HTTPException(status_code=404, detail="No processing job found for this dataset")
    return job

@router.get("/{dataset_id}/statistics", response_model=DatasetStatisticsResponse)
def get_dataset_statistics(
    dataset_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id, Dataset.owner_id == current_user.id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    stats = db.query(DatasetStatistics).filter(DatasetStatistics.dataset_id == dataset_id).first()
    if not stats:
        raise HTTPException(status_code=404, detail="Statistics not found for this dataset")
    return stats

@router.get("/{dataset_id}/columns/statistics", response_model=List[ColumnStatisticsResponse])
def get_column_statistics(
    dataset_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id, Dataset.owner_id == current_user.id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    stats = db.query(ColumnStatistics).filter(ColumnStatistics.dataset_id == dataset_id).all()
    return stats
