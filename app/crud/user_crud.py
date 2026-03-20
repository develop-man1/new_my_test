from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from typing import Optional

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


class UserCrud:
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
    
    async def user_create(self, user_data: UserCreate) -> User:
        
        new_user = User(**user_data.model_dump())
        
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
    
    
    async def user_update(self, id: int, user_data: UserUpdate) -> Optional[User]:
        
        stmt = update(User).where(User.id == id).values(**user_data.model_dump(exclude_unset=True)).returning(User)
        result = await self.db.execute(stmt)
        
        await self.db.commit()
        
        return result.scalar_one_or_none()
    
    
    async def user_delete(self, id: int) -> Optional[User]:
        
        stmt = delete(User).where(User.id == id).returning(User)
        result = await self.db.execute(stmt)
        
        deleted_user = result.scalar_one_or_none()
        
        await self.db.commit()
        
        return deleted_user