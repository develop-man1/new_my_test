from pydantic import BaseModel, Field
from typing import Literal


class PermissionCreate(BaseModel):
    
    resources: str = Field(...)
    action: Literal["create, read, update, delete"]
    

class PermissionResponse(BaseModel):
    
    id: int = Field(...)
    resources: str
    action: Literal["create, read, update, delete"]