from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from ..core.database import Base


class Role(Base):
    
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text)
    
    permissions = relationship("Permission", secondary="role_permission")