from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from backend.app.utils.bson import PyObjectId


class UserInDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True

    class Config:
        allow_population_by_field_name = True
        json_encoders = {PyObjectId: str}
        orm_mode = True
