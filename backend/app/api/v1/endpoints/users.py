from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies.database import get_db
from app.api.dependencies.auth import get_current_active_user, require_role
from app.schemas.user import UserResponse, UserUpdate, UserUpdatePassword
from app.schemas.common import StandardResponse
from app.models.user import User
from app.services.user import UserService
from app.models.enums import UserRole

router = APIRouter()

@router.get("/me", response_model=StandardResponse[UserResponse])
def read_user_me(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    return StandardResponse(success=True, message="Profile fetched", data=UserResponse.model_validate(current_user))

@router.patch("/me", response_model=StandardResponse[UserResponse])
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    user = UserService.update_user(db, user=current_user, user_in=user_in)
    return StandardResponse(success=True, message="Profile updated", data=UserResponse.model_validate(user))

@router.patch("/change-password", response_model=StandardResponse)
def change_password(
    *,
    db: Session = Depends(get_db),
    password_in: UserUpdatePassword,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    UserService.change_password(db, user=current_user, password_in=password_in)
    return StandardResponse(success=True, message="Password updated successfully")
