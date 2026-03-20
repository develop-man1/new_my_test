from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from ..core.database import get_db
from ..schemas.role import RoleCreate, RoleResponse
from ..schemas.permission import PermissionCreate, PermissionResponse
from ..services.role_service import RoleService
from ..services.permission_service import PermissionService
from ..dependencies.auth import get_admin_user
from ..models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(role_data: RoleCreate, db: AsyncSession = Depends(get_db), _: User = Depends(get_admin_user)):
    
    service = RoleService(db)
    
    return await service.role_create(role_data)


@router.post("/permissions", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
async def create_permission(permission_data: PermissionCreate, db: AsyncSession = Depends(get_db), _: User = Depends(get_admin_user)):
    
    service = PermissionService(db)
    
    return await service.create_permission(permission_data)