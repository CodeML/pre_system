from sqlalchemy import Column, String, Text, Table, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base, BaseModel


# 角色-权限 关联表
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)


class Permission(BaseModel):
    __tablename__ = "permissions"

    code = Column(String(100), unique=True, index=True, comment="权限编码，例如: project:create")
    name = Column(String(100), nullable=True, comment="权限显示名")
    description = Column(Text, nullable=True, comment="权限描述")

    def __repr__(self):
        return f"<Permission {self.code}>"
