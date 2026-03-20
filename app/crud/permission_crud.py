from sqlalchemy.ext.asyncio import AsyncSession

from ..models.permission import Permission
from ..schemas.permission import PermissionCreate


class PermissionCrud:
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
        
    async def permission_create(self, permission_data: PermissionCreate) -> Permission:
        
        new_permission = Permission(**permission_data.model_dump())
        
        self.db.add(new_permission)
        await self.db.commit()
        await self.db.refresh(new_permission)
        return new_permission