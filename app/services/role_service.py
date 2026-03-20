from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from ..crud.role_crud import RoleCrud
from ..schemas.role import RoleCreate, RoleResponse


class RoleService:
    
    def __init__(self, db: AsyncSession):
        self.role_crud = RoleCrud(db)
        
    
    async def role_create(self, role_data: RoleCreate) -> RoleResponse:
        
        existing_role = await self.role_crud.get_role_by_name(role_data.name)
        
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role already exist"
            )
        
        role = await self.role_crud.role_create(role_data)
        
        return RoleResponse.model_validate(role)