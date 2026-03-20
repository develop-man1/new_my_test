from pydantic import BaseModel, Field
from typing import Optional


class RoleCreate(BaseModel):
    
    name: str = Field(...)
    description: str = Field(...)
    
    
class RoleResponse(BaseModel):
    
    id: int = Field(...)
    name: str
    description: Optional[str] = None