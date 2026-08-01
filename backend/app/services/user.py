from sqlalchemy.orm import Session
from app.db.repositories.user import user_repo
from app.schemas.user import UserCreate, UserUpdate, UserUpdatePassword
from app.models.user import User
from app.core.exceptions import BaseAppException
from app.core.security import verify_password, get_password_hash
from fastapi import status

class UserService:
    @staticmethod
    def create_user(db: Session, *, user_in: UserCreate) -> User:
        user = user_repo.get_by_email(db, email=user_in.email)
        if user:
            raise BaseAppException(
                message="The user with this email already exists in the system.",
                status_code=status.HTTP_409_CONFLICT
            )
            
        user = user_repo.get_by_username(db, username=user_in.username)
        if user:
            raise BaseAppException(
                message="The user with this username already exists in the system.",
                status_code=status.HTTP_409_CONFLICT
            )
            
        return user_repo.create(db, obj_in=user_in)

    @staticmethod
    def update_user(db: Session, *, user: User, user_in: UserUpdate) -> User:
        if user_in.email and user_in.email != user.email:
            existing_user = user_repo.get_by_email(db, email=user_in.email)
            if existing_user:
                raise BaseAppException(
                    message="The user with this email already exists in the system.",
                    status_code=status.HTTP_409_CONFLICT
                )
        return user_repo.update(db, db_obj=user, obj_in=user_in)

    @staticmethod
    def change_password(db: Session, *, user: User, password_in: UserUpdatePassword) -> User:
        if not verify_password(password_in.current_password, user.hashed_password):
            raise BaseAppException(
                message="Incorrect current password.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        hashed_password = get_password_hash(password_in.new_password)
        user.hashed_password = hashed_password
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
