from typing import Optional
import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.models.enums import UserRole, Status
from app.core.security import validate_password_strength

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    display_name: Optional[str] = Field(None, max_length=100)
    timezone: str = "UTC"
    preferred_theme: str = "light"
    preferred_language: str = "en"

class UserCreate(UserBase):
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not validate_password_strength(v):
            raise ValueError(
                "Password must be at least 12 characters and contain an uppercase letter, "
                "a lowercase letter, a number, and a special character."
            )
        return v
    
    @field_validator('username')
    @classmethod
    def sanitize_username(cls, v: str) -> str:
        return v.strip().lower()

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    display_name: Optional[str] = Field(None, max_length=100)
    timezone: Optional[str] = None
    preferred_theme: Optional[str] = None
    preferred_language: Optional[str] = None

class UserUpdatePassword(BaseModel):
    current_password: str
    new_password: str

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not validate_password_strength(v):
            raise ValueError(
                "Password must be at least 12 characters and contain an uppercase letter, "
                "a lowercase letter, a number, and a special character."
            )
        return v

class UserResponse(UserBase):
    id: uuid.UUID
    role: UserRole
    status: Status
    profile_image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    email_verified: bool

    class Config:
        from_attributes = True

class LoginData(BaseModel):
    email: EmailStr
    password: str

class ResetPassword(BaseModel):
    token: str
    new_password: str

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not validate_password_strength(v):
            raise ValueError("Password is not strong enough")
        return v
