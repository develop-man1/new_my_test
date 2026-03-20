from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class RoleCreate(BaseModel):
    
    name: str = Field(...)
    description: str = Field(...)
    
    
class RoleResponse(BaseModel):
    
    id: int = Field(...)
    name: str
    description: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)