from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from ..core.database import get_db
from ..core.security import get_current_user
from ..crud.user_crud import UserCrud
from ..models.user import User


async def get_active_user(user_id: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> User:
    
    user_crud = UserCrud(db)
    user = await user_crud.get_user_by_id(int(user_id))
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is deactivated"
        )
    
    return user


async def get_admin_user(current_user: User = Depends(get_active_user)) -> User:
    
    if current_user.role.name != "admin":  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: admins only"
        )
    
    return current_user


def require_permission(resource: str, action: str):
    
    async def permission_checker(
        current_user: User = Depends(get_active_user)) -> User:
        
        user_permissions = current_user.role.permissions  # type: ignore
        
        has_access = any(p.resource == resource and p.action == action for p in user_permissions)
        
        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: no '{action}' permission on '{resource}'"
            )
        
        return current_user
    
    return permission_checker