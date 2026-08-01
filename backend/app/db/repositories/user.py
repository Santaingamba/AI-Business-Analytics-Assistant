from typing import Optional
from sqlalchemy.orm import Session
from app.db.repository import BaseRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()
        
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        # Override create to handle password hashing
        from app.core.security import get_password_hash
        
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            display_name=obj_in.display_name,
            hashed_password=get_password_hash(obj_in.password),
            timezone=obj_in.timezone,
            preferred_theme=obj_in.preferred_theme,
            preferred_language=obj_in.preferred_language,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

user_repo = UserRepository(User)
