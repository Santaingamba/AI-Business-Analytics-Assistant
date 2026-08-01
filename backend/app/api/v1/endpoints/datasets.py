import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, Form, UploadFile, File, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.dependencies.auth import get_current_active_user
from app.models.user import User
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetResponse, DatasetDetailsResponse, DatasetPreviewResponse
from app.services.dataset import DatasetService
from app.db.repositories.dataset import dataset_repo
from app.core.exceptions import BaseAppException

router = APIRouter()

@router.post("/upload", response_model=DatasetResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    display_name: str = Form(""),
    description: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    return await DatasetService.upload_dataset(
        db=db,
        user_id=current_user.id,
        file=file,
        display_name=display_name,
        description=description
    )

@router.get("", response_model=List[DatasetResponse])
def list_datasets(
    skip: int = 0,
    limit: int = Query(100, le=100),
    search: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    return dataset_repo.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit, search=search
    )

@router.get("/{dataset_id}", response_model=DatasetDetailsResponse)
def get_dataset(
    dataset_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    dataset = dataset_repo.get_active_by_id_and_owner(db, id=dataset_id, owner_id=current_user.id)
    if not dataset:
        raise BaseAppException("Dataset not found", status.HTTP_404_NOT_FOUND)
    return dataset

@router.get("/{dataset_id}/preview", response_model=DatasetPreviewResponse)
def get_dataset_preview(
    dataset_id: uuid.UUID,
    rows: int = Query(20, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    dataset = dataset_repo.get_active_by_id_and_owner(db, id=dataset_id, owner_id=current_user.id)
    if not dataset:
        raise BaseAppException("Dataset not found", status.HTTP_404_NOT_FOUND)
        
    headers, data = DatasetService.get_preview(dataset, num_rows=rows)
    return {
        "headers": headers,
        "data": data,
        "row_count": len(data),
        "column_count": len(headers)
    }

@router.delete("/{dataset_id}")
def delete_dataset(
    dataset_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    dataset = dataset_repo.get_active_by_id_and_owner(db, id=dataset_id, owner_id=current_user.id)
    if not dataset:
        raise BaseAppException("Dataset not found", status.HTTP_404_NOT_FOUND)
        
    DatasetService.delete_dataset(db, dataset=dataset)
    return {"success": True, "message": "Dataset deleted successfully"}
