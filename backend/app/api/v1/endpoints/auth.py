from typing import Any
from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session
from app.api.dependencies.database import get_db
from app.schemas.user import UserCreate, UserResponse, LoginData
from app.schemas.token import Token
from app.schemas.common import StandardResponse
from app.services.user import UserService
from app.services.auth import AuthService
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=StandardResponse[UserResponse])
def register(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate
) -> Any:
    user = UserService.create_user(db, user_in=user_in)
    return StandardResponse(success=True, message="User registered successfully", data=UserResponse.model_validate(user))

@router.post("/login", response_model=StandardResponse[Token])
def login(
    response: Response,
    *,
    db: Session = Depends(get_db),
    login_data: LoginData
) -> Any:
    user = AuthService.authenticate(db, login_data=login_data)
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    # Store refresh token in secure HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60
    )
    
    return StandardResponse(
        success=True, 
        message="Login successful", 
        data=Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)
    )

@router.post("/logout", response_model=StandardResponse)
def logout(response: Response) -> Any:
    response.delete_cookie(key="refresh_token")
    return StandardResponse(success=True, message="Logout successful")

@router.post("/refresh", response_model=StandardResponse[Token])
async def refresh(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
) -> Any:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        try:
            body = await request.json()
            refresh_token = body.get("refresh_token")
        except:
            pass
        
    if not refresh_token:
        return StandardResponse(success=False, message="Refresh token missing", data=None)

    payload = decode_token(refresh_token)
    user_id = payload.get("sub")
    if not user_id or payload.get("type") != "refresh":
        return StandardResponse(success=False, message="Invalid refresh token", data=None)

    access_token = create_access_token(user_id)
    new_refresh_token = create_refresh_token(user_id)
    
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60
    )
    
    return StandardResponse(
        success=True, 
        message="Token refreshed", 
        data=Token(access_token=access_token, token_type="bearer", refresh_token=new_refresh_token)
    )
