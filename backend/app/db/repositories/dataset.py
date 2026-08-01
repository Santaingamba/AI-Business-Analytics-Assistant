from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.repository import BaseRepository
from app.models.dataset import Dataset
from app.models.dataset_column import DatasetColumn
from app.schemas.dataset import DatasetCreate, DatasetUpdate
import uuid

class DatasetRepository(BaseRepository[Dataset, DatasetCreate, DatasetUpdate]):
    def get_by_checksum_and_owner(self, db: Session, *, checksum: str, owner_id: uuid.UUID) -> Optional[Dataset]:
        return db.query(Dataset).filter(
            Dataset.checksum_sha256 == checksum,
            Dataset.owner_id == owner_id,
            Dataset.deleted_at == None
        ).first()

    def get_active_by_id_and_owner(self, db: Session, *, id: uuid.UUID, owner_id: uuid.UUID) -> Optional[Dataset]:
        return db.query(Dataset).filter(
            Dataset.id == id,
            Dataset.owner_id == owner_id,
            Dataset.deleted_at == None
        ).first()

    def get_multi_by_owner(
        self, db: Session, *, owner_id: uuid.UUID, skip: int = 0, limit: int = 100, search: str = None
    ) -> List[Dataset]:
        query = db.query(Dataset).filter(
            Dataset.owner_id == owner_id,
            Dataset.deleted_at == None
        )
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Dataset.display_name.ilike(search_term),
                    Dataset.original_filename.ilike(search_term)
                )
            )
        return query.order_by(Dataset.created_at.desc()).offset(skip).limit(limit).all()

    def count_by_owner(self, db: Session, *, owner_id: uuid.UUID, search: str = None) -> int:
        query = db.query(Dataset).filter(
            Dataset.owner_id == owner_id,
            Dataset.deleted_at == None
        )
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Dataset.display_name.ilike(search_term),
                    Dataset.original_filename.ilike(search_term)
                )
            )
        return query.count()

class DatasetColumnRepository:
    def create_multi(self, db: Session, *, dataset_id: uuid.UUID, columns_in: List[dict]):
        db_columns = [
            DatasetColumn(
                dataset_id=dataset_id,
                **col
            )
            for col in columns_in
        ]
        db.add_all(db_columns)
        db.commit()

dataset_repo = DatasetRepository(Dataset)
dataset_column_repo = DatasetColumnRepository()
