import uuid
from sqlalchemy import String, Boolean, Enum as SQLEnum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.enums import ColumnDataType

class DatasetColumn(Base):
    __tablename__ = "dataset_columns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("datasets.id", ondelete="CASCADE"), index=True, nullable=False)
    
    column_name: Mapped[str] = mapped_column(String(255), nullable=False)
    detected_data_type: Mapped[ColumnDataType] = mapped_column(SQLEnum(ColumnDataType), default=ColumnDataType.UNKNOWN, nullable=False)
    
    is_nullable: Mapped[bool] = mapped_column(Boolean, default=True)
    is_unique: Mapped[bool] = mapped_column(Boolean, default=False)
    sample_values: Mapped[str] = mapped_column(String(1000), nullable=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    dataset = relationship("Dataset", back_populates="columns")
