from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from ..crud.user_crud import UserCrud
from ..core.security import verify_password, create_access_token
from ..schemas.user import LoginRequest


class AuthService:
    
    def __init__(self, db: AsyncSession):
        self.user_crud = UserCrud(db)
    
    
    async def login(self, login_data: LoginRequest) -> dict:
        
        user = await self.user_crud.get_user_by_email(login_data.email)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        if not user.is_active: # type: ignore
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is deactivate"
            )
        
        if not verify_password(login_data.password, user.password): # type: ignore
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        token = create_access_token(subject=str(user.id))
        
        return {"access_token": token, "token_type": "bearer"}