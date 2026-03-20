from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum


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
    repeat_password = password
    role: RoleEnum = RoleEnum.user
    
class UserResponse(BaseModel):
    
    id: int = Field(...)
    name: str
    surname: str
    patronymic: str
    email: str
    role: RoleEnum
    created_at: datetime
    is_active = True
    
    
class UserUpdate(BaseModel):
    
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    
    
class LoginRequest(BaseModel):
    
    email: str = Field(...)
    password: str = Field(...)