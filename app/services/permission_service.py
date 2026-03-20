from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.permission_crud import PermissionCrud
from ..schemas.permission import PermissionCreate, PermissionResponse


class PermissionService:
    
    def __init__(self, db: AsyncSession):
        self.permission_crud = PermissionCrud(db)
    
    
    async def create_permission(self, permission_data: PermissionCreate) -> PermissionResponse:
        
        permission = await self.permission_crud.permission_create(permission_data)
        
        return PermissionResponse.model_validate(permission)