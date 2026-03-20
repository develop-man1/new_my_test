from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from ..core.database import get_db
from ..schemas.user import UserCreate, UserResponse, LoginRequest
from ..services.auth_service import AuthService
from ..services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    
    service = UserService(db)
    
    return await service.user_create(user_data)


@router.post("/login")
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    
    service = AuthService(db)
    
    return await service.login(login_data)


@router.post("/logout")
async def logout():
    return {"message": "Successfully log out!"}