from sqlalchemy import Column, Integer, String, DateTime, func, Text, ForeignKey
from sqlalchemy.orm import relationship

from ..core.database import Base


class User(Base):
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(Text, nullable=False)
    repeat_password = Column(Text, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    
    created_at = Column(DateTime, server_default=func.now())
    
    