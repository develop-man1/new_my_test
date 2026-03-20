from sqlalchemy.ext.asyncio import AsyncSession

from ..models.role import Role
from ..schemas.role import RoleCreate


class RoleCrud:
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
    
    async def role_create(self, role_data: RoleCreate) -> Role:
        
        new_role = Role(**role_data.model_dump())
        
        self.db.add(new_role)
        await self.db.commit()
        await self.db.refresh(new_role)
        return new_role