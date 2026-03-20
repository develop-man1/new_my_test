from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


class PermissionCreate(BaseModel):
    
    resource: str = Field(...)
    action: Literal["create", "read", "update", "delete"]
    

class PermissionResponse(BaseModel):
    
    id: int = Field(...)
    resource: str
    action: Literal["create", "read", "update", "delete"]
    
    model_config = ConfigDict(from_attributes=True)