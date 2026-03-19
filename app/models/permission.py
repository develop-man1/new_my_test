from sqlalchemy import Column, Integer, String, UniqueConstraint

from ..core.database import Base


class Permission(Base):
    
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    resource = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False, index=True)
    
    __table_args__ = (UniqueConstraint("resource", "action"),)