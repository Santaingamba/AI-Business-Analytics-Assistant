import uuid
import time
from datetime import datetime, timezone
import pandas as pd
from sqlalchemy.orm import Session

from app.models.processing import ProcessingJob, DatasetStatistics, ColumnStatistics
from app.models.dataset import Dataset
from app.models.dataset_column import DatasetColumn
from app.services.storage.local import LocalStorageService
from app.services.processing.profiler import ProfilingService

class ProcessingOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.storage_service = LocalStorageService()
        
    def create_job(self, dataset_id: uuid.UUID, user_id: uuid.UUID = None) -> ProcessingJob:
        job = ProcessingJob(
            dataset_id=dataset_id,
            status="PENDING",
            processing_version="1.0.0",
            created_by=user_id
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def run_profiling(self, job_id: uuid.UUID):
        job = self.db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
        if not job:
            return
            
        job.status = "RUNNING"
        job.started_at = datetime.now(timezone.utc)
        self.db.commit()
        
        start_time = time.time()
        
        try:
            dataset = self.db.query(Dataset).filter(Dataset.id == job.dataset_id).first()
            if not dataset:
                raise ValueError("Dataset not found")
                
            file_path = self.storage_service.get_file_path(dataset.stored_filename)
            
            if dataset.file_type == "CSV":
                df = pd.read_csv(file_path, low_memory=False)
            elif dataset.file_type == "EXCEL":
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported format: {dataset.file_type}")
                
            profile = ProfilingService.profile_dataset(df)
            
            # Save Dataset Stats
            ds_stats = self.db.query(DatasetStatistics).filter(DatasetStatistics.dataset_id == dataset.id).first()
            if not ds_stats:
                ds_stats = DatasetStatistics(dataset_id=dataset.id)
                self.db.add(ds_stats)
            
            d_profile = profile["dataset"]
            for key, val in d_profile.items():
                if hasattr(ds_stats, key):
                    setattr(ds_stats, key, val)
                    
            # Save Column Stats
            col_profiles = profile["columns"]
            db_columns = self.db.query(DatasetColumn).filter(DatasetColumn.dataset_id == dataset.id).all()
            name_to_id = {c.column_name: c.id for c in db_columns}
            
            for col_name, c_profile in col_profiles.items():
                col_id = name_to_id.get(col_name)
                if not col_id:
                    continue
                    
                c_stats = self.db.query(ColumnStatistics).filter(
                    ColumnStatistics.column_id == col_id
                ).first()
                
                if not c_stats:
                    c_stats = ColumnStatistics(dataset_id=dataset.id, column_id=col_id)
                    self.db.add(c_stats)
                    
                for key, val in c_profile.items():
                    if hasattr(c_stats, key):
                        setattr(c_stats, key, val)
            
            duration_ms = int((time.time() - start_time) * 1000)
            job.duration_ms = duration_ms
            job.completed_at = datetime.now(timezone.utc)
            job.status = "COMPLETED"
            
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            job = self.db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
            if job:
                job.status = "FAILED"
                job.summary = {"error": str(e)}
                job.completed_at = datetime.now(timezone.utc)
                job.duration_ms = int((time.time() - start_time) * 1000)
                self.db.commit()
