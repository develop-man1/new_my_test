from sqlalchemy import Column, Integer, ForeignKey

from ..core.database import Base


class RolePermission(Base):
    
    __tablename__ = "role_permissions"
    
    role_id = Column(Integer, ForeignKey("roles.id"))
    permission_id = Column(Integer, ForeignKey("permissions.id"))