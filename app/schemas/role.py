from pydantic import BaseModel, Field


class RoleCreate(BaseModel):
    
    name: str = Field(...)
    description: str = Field(...)
    
    
class RoleResponse(BaseModel):
    
    id: int = Field(...)
    name: str
    description: str