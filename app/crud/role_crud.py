from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from ..models.role import Role
from ..schemas.role import RoleCreate


class RoleCrud:
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
    
    async def get_role_by_name(self, name: str) -> Optional[Role]:
        
        stmt = select(Role).where(Role.name == name)
        result = await self.db.execute(stmt)
        
        return result.scalar_one_or_none()
        
    
    async def role_create(self, role_data: RoleCreate) -> Role:
        
        new_role = Role(**role_data.model_dump())
        
        self.db.add(new_role)
        await self.db.commit()
        await self.db.refresh(new_role)
        return new_role