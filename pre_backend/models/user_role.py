from sqlalchemy import Column, Integer, ForeignKey
from models.base import BaseModel


class UserRole(BaseModel):
    __tablename__ = "user_roles"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, comment="用户ID")
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), index=True, comment="角色ID")
