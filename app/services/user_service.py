from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from ..crud.user_crud import UserCrud
from ..crud.role_crud import RoleCrud
from ..schemas.user import UserResponse, UserCreate, UserUpdate
from ..core.security import hash_password
from ..models.user import User


class UserService:
    
    def __init__(self, db: AsyncSession):
        self.user_crud = UserCrud(db)
        self.role_crud = RoleCrud(db)
        
        
    async def get_user_by_id(self, user_id: int) -> UserResponse:
        
        current_user = await self.user_crud.get_user_by_id(user_id)
        
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        return UserResponse.model_validate(current_user)
    
    
    async def get_user_by_email(self, email: str) -> UserResponse:
        
        user_email = await self.user_crud.get_user_by_email(email)
        
        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email not found"
            )
            
        return UserResponse.model_validate(user_email)
    
    
    async def user_create(self, user_data: UserCreate) -> UserResponse:
        
        existing_user = await self.user_crud.get_user_by_email(user_data.email)
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exist"
            )
            
        role = await self.role_crud.get_role_by_name(user_data.role.value)
        
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
            
        hashed_password = hash_password(user_data.password)
        
        new_user = await self.user_crud.user_create(user_data=user_data, hashed_password=hashed_password, role_id=role.id) # type: ignore
        
        return UserResponse.model_validate(new_user)
    
    
    async def update_user(self, current_user: User, user_data: UserUpdate) -> UserResponse:
        
        if user_data.password:
            user_data.password = hash_password(user_data.password)
            
        updated_user = await self.user_crud.user_update(id=current_user.id, user_data=user_data) # type: ignore
        
        if updated_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        return UserResponse.model_validate(updated_user)
    
    
    async def delete_user(self, user_id: int) -> None:
        
        existing_user = await self.user_crud.get_user_by_id(user_id)
        
        if existing_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        await self.user_crud.user_delete(user_id)