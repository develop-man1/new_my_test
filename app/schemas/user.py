from pydantic import BaseModel, Field, EmailStr, model_validator, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum

from .role import RoleResponse


class RoleEnum(str, Enum):
    
    admin = "admin"
    moderator = "moderator"
    user = "user"


class UserCreate(BaseModel):
    
    name: str = Field(...)
    surname: str = Field(...)
    patronymic: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)
    repeat_password: str = Field(...)
    role: RoleEnum = RoleEnum.user
    
    @model_validator(mode="after")
    def password_comparison(self):
        if self.password != self.repeat_password:
            raise ValueError("Password dont match")
        return self
    
class UserResponse(BaseModel):
    
    id: int = Field(...)
    name: str
    surname: str
    patronymic: str
    email: str
    role: RoleResponse
    created_at: datetime
    is_active: bool = True
    
    model_config = ConfigDict(from_attributes=True)
    
    
class UserUpdate(BaseModel):
    
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    
    
class LoginRequest(BaseModel):
    
    email: str = Field(...)
    password: str = Field(...)