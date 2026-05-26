from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., description="用户名")
    name: Optional[str] = Field(None, description="姓名/昵称")
    phone: Optional[str] = Field(None, description="手机号")
    is_active: Optional[bool] = Field(True, description="账户是否启用")


class UserCreate(UserBase):
    password: str = Field(..., description="登录密码")


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, description="更新后的姓名/昵称")
    phone: Optional[str] = Field(None, description="更新后的手机号")
    is_active: Optional[bool] = Field(None, description="启用/禁用账户")


class UserRead(UserBase):
    id: int = Field(..., description="用户ID")
    create_time: Optional[datetime] = Field(None, description="创建时间")
    update_time: Optional[datetime] = Field(None, description="最后更新时间")

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str = Field(..., description="JWT 访问令牌")
    token_type: str = Field("bearer", description="令牌类型")


class TokenWithUser(Token):
    user: UserRead = Field(..., description="用户信息")
    roles: List[str] = Field(default=[], description="用户角色代码列表")
    permissions: List[str] = Field(default=[], description="权限编码列表")
    org_id: int = Field(1, description="当前所属组织ID")


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., description="新密码")
    confirm_password: str = Field(..., description="确认新密码")

    def __init__(self, **data):
        super().__init__(**data)
        if self.new_password != self.confirm_password:
            raise ValueError("新密码和确认密码不一致")


class ChangePasswordResponse(BaseModel):
    success: bool = True
    message: str = "密码修改成功"

