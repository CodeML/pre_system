from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship
from models.base import BaseModel
from models.permission import role_permissions, Permission


class Role(BaseModel):
    __tablename__ = "roles"

    name = Column(String(50), unique=True, index=True, comment="角色名称")
    code = Column(String(50), unique=True, index=True, comment="角色编码")
    # legacy 文本字段，保留以兼容旧数据
    permission = Column(Text, nullable=True, comment="权限描述（JSON格式）")
    is_active = Column(Boolean, default=True, comment="是否启用")

    # 结构化关系：角色拥有多个权限
    permissions = relationship("Permission", secondary=role_permissions, backref="roles")
