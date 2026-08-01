import uuid
from typing import List
from sqlalchemy.orm import Session
from app.models.ai import AIRecommendation
from app.models.enums import ImportanceLevel, RecommendationStatus

class RecommendationGenerator:
    """Extracts and persists structured business recommendations."""
    
    def __init__(self, db: Session):
        self.db = db
        
    def store_recommendations(self, dataset_id: uuid.UUID, recommendations: List[dict]) -> List[AIRecommendation]:
        saved_recs = []
        for rec in recommendations:
            try:
                priority = ImportanceLevel(rec.get("priority", "MEDIUM").upper())
            except ValueError:
                priority = ImportanceLevel.MEDIUM
                
            db_rec = AIRecommendation(
                dataset_id=dataset_id,
                priority=priority,
                recommendation=rec.get("recommendation", ""),
                business_impact=rec.get("business_impact", ""),
                confidence=float(rec.get("confidence", 0.0)),
                status=RecommendationStatus.NEW
            )
            self.db.add(db_rec)
            saved_recs.append(db_rec)
        self.db.commit()
        return saved_recs
