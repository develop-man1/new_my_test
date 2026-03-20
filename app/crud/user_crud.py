from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Optional

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


class UserCrud:
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
        
    async def get_user_by_id(self, id: int) -> Optional[User]:
        
        stmt = select(User).where(User.id == id)
        result = await self.db.execute(stmt)
        
        return result.scalar_one_or_none()
    
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        
        return result.scalar_one_or_none()
        
    
    async def user_create(self, user_data: UserCreate, hashed_password: str, role_id: int) -> User:
        
        data = user_data.model_dump(exclude={"password", "repeat_password", "role"})
        
        new_user = User(**data, password=hashed_password, role_id=role_id)
        
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
        
        stmt = update(User).where(User.id == id).values(is_active=False).returning(User)
        result = await self.db.execute(stmt)
        
        await self.db.commit()
        
        return result.scalar_one_or_none()