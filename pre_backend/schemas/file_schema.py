from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FileCreate(BaseModel):
    """创建文件请求"""
    task_id: int = Field(..., description="任务ID")
    name: str = Field(..., description="文件名称")
    url: str = Field(..., description="文件URL")
    file_type: str = Field(..., description="文件类型")
    file_format: Optional[str] = Field(None, description="文件格式")
    size: Optional[float] = Field(None, description="文件大小MB")
    material_id: Optional[int] = Field(None, description="关联素材ID")
    description: Optional[str] = Field(None, description="描述")


class FileRead(BaseModel):
    """文件读取响应"""
    id: int = Field(..., description="文件ID")
    task_id: int = Field(..., description="所属任务ID")
    name: str = Field(..., description="文件名称")
    url: str = Field(..., description="文件下载/访问URL")
    file_type: str = Field(..., description="文件类型")
    version: str = Field(..., description="版本号")
    is_confirm: bool = Field(False, description="客户是否确认")
    confirm_time: Optional[datetime] = Field(None, description="确认时间")
    upload_time: datetime = Field(..., description="上传时间")

    class Config:
        from_attributes = True


class FileUpdate(BaseModel):
    """文件更新请求"""
    name: Optional[str] = Field(None, description="文件名称")
    description: Optional[str] = Field(None, description="描述")
    is_active: Optional[bool] = Field(None, description="是否活跃")


class FileConfirm(BaseModel):
    """文件确认请求"""
    confirm_remark: Optional[str] = Field(None, description="确认备注")
