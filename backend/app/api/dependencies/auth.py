from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import decode_token
from app.core.exceptions import BaseAppException
from app.models.user import User
from app.models.enums import UserRole, Status
from app.db.repositories.user import user_repo
from app.api.dependencies.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = BaseAppException(
        message="Could not validate credentials",
        status_code=status.HTTP_401_UNAUTHORIZED
    )
    
    payload = decode_token(token)
    user_id_str: str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception
        
    import uuid
    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise credentials_exception
        
    user = user_repo.get(db, id=user_id)
    if user is None:
        raise credentials_exception
        
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.status != Status.ACTIVE:
        # If they are pending verification or locked, they shouldn't pass this
        raise BaseAppException(
            message=f"User is {current_user.status.value.lower()}",
            status_code=status.HTTP_403_FORBIDDEN
        )
    return current_user

def require_role(allowed_roles: list[UserRole]):
    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in allowed_roles:
            raise BaseAppException(
                message="You do not have enough privileges",
                status_code=status.HTTP_403_FORBIDDEN
            )
        return current_user
    return role_checker
