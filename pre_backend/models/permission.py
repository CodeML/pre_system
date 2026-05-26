from sqlalchemy import Column, String, Text, Table, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base, BaseModel
from datetime import datetime


# 角色-权限 关联表
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)
)

# 用户-特权/委派权限 关联表（用于上级给下级临时赋权）
user_permissions = Table(
    "user_permissions",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
    Column("granted_by", Integer, ForeignKey("users.id"), nullable=True, comment="授权人ID"),
    Column("grant_time", DateTime, default=datetime.utcnow)
)



class Permission(BaseModel):
    """
    权限模型：资源 + 动作 + 作用域
    """
    __tablename__ = "permissions"

    code = Column(String(100), unique=True, index=True, comment="权限编码，例如: project:create")
    name = Column(String(100), nullable=True, comment="权限显示名")
    
    # 核心增强：数据作用域
    # scope 类型：all(全量), self(仅自己), team(所属组), related(参与的)
    data_scope = Column(String(20), default="all", comment="数据可见性范围")
    
    description = Column(Text, nullable=True, comment="权限描述")

    def __repr__(self):
        return f"<Permission {self.code}>"
