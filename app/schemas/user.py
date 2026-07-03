from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from backend.app.utils.bson import PyObjectId


class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserOut(BaseModel):
    id: PyObjectId = Field(..., alias="_id")
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool

    class Config:
        allow_population_by_field_name = True
        json_encoders = {PyObjectId: str}
