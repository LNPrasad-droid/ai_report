from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class AuthenticatedUser(BaseModel):
    uid: str
    email: EmailStr
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    provider: Optional[str] = None
    email_verified: bool = False
    role: str = Field(default="Viewer")
    status: str = Field(default="active")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None


class UserCreatePayload(BaseModel):
    uid: str
    email: EmailStr
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    provider: Optional[str] = None
    email_verified: bool = False


class UserProfileUpdate(BaseModel):
    display_name: Optional[str] = None
    photo_url: Optional[str] = None


class AuthResponse(BaseModel):
    uid: str
    email: EmailStr
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    role: str
    status: str
    provider: Optional[str] = None
    email_verified: bool
    last_login: Optional[datetime] = None
