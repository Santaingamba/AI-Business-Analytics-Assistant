from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from app.db.repositories.user import user_repo
from app.schemas.user import LoginData
from app.models.user import User
from app.models.enums import Status
from app.core.exceptions import BaseAppException
from app.core.security import verify_password
from app.core.config import settings
from fastapi import status

class AuthService:
    @staticmethod
    def authenticate(db: Session, *, login_data: LoginData) -> User:
        user = user_repo.get_by_email(db, email=login_data.email)
        if not user:
            raise BaseAppException(
                message="Incorrect email or password",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
            
        if user.status in (Status.LOCKED, Status.SUSPENDED):
            locked_until = user.account_locked_until
            if locked_until and locked_until.tzinfo is None:
                locked_until = locked_until.replace(tzinfo=timezone.utc)
                
            if locked_until and locked_until > datetime.now(timezone.utc):
                raise BaseAppException(
                    message="Account is locked due to too many failed login attempts.",
                    status_code=status.HTTP_403_FORBIDDEN
                )
            elif user.status == Status.LOCKED:
                # Lock expired, reset
                user.status = Status.ACTIVE
                user.failed_login_attempts = 0
                user.account_locked_until = None
                db.add(user)
                db.commit()

        if not verify_password(login_data.password, user.hashed_password):
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
                user.status = Status.LOCKED
                user.account_locked_until = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCOUNT_LOCKOUT_MINUTES)
            db.add(user)
            db.commit()
            raise BaseAppException(
                message="Incorrect email or password",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
            
        # Success login
        user.failed_login_attempts = 0
        user.account_locked_until = None
        user.last_login = datetime.now(timezone.utc)
        db.add(user)
        db.commit()
        return user
