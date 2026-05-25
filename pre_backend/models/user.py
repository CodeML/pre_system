from sqlalchemy import Column, String, Boolean
from models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    username = Column(String(50), unique=True, index=True, comment="登录账号")
    password = Column(String(100), comment="加密密码")
    name = Column(String(50), comment="真实姓名")
    phone = Column(String(20), nullable=True, comment="联系方式")
    is_active = Column(Boolean, default=True, comment="是否启用")
    is_outsourced = Column(Boolean, default=False, comment="是否为外协人员")