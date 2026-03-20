from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from ..core.database import get_db
from ..schemas.user import UserResponse, UserUpdate
from ..services.user_service import UserService
from ..dependencies.auth import get_active_user
from ..models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_active_user)):
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_me(user_data: UserUpdate, current_user: User = Depends(get_active_user), db: AsyncSession = Depends(get_db)):
    
    service = UserService(db)
    
    return await service.update_user(current_user, user_data)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(current_user: User = Depends(get_active_user), db: AsyncSession = Depends(get_db)):
    
    service = UserService(db)
    
    await service.delete_user(current_user.id)  # type: ignore