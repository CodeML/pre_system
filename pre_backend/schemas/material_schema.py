from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MaterialCreate(BaseModel):
    """创建素材请求"""
    name: str = Field(..., description="素材名称")
    type: str = Field(..., description="素材类型")
    url: str = Field(..., description="素材URL")
    category: Optional[str] = Field(None, description="分类")
    file_format: Optional[str] = Field(None, description="文件格式")
    size: Optional[int] = Field(None, description="文件大小KB")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    is_reusable: Optional[bool] = Field(True, description="是否可复用")
    description: Optional[str] = Field(None, description="描述")


class MaterialRead(BaseModel):
    """素材读取响应"""
    id: int = Field(..., description="素材ID")
    name: str = Field(..., description="素材名称")
    type: str = Field(..., description="素材类型")
    url: str = Field(..., description="素材URL地址")
    category: Optional[str] = Field(None, description="分类")
    is_reusable: bool = Field(True, description="是否可复用")
    reuse_count: int = Field(0, description="复用次数")
    project_ids: Optional[List[int]] = Field(None, description="关联项目ID列表")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    create_time: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True


class MaterialUpdate(BaseModel):
    """更新素材请求"""
    name: Optional[str] = Field(None, description="素材名称")
    category: Optional[str] = Field(None, description="分类")
    is_reusable: Optional[bool] = Field(None, description="是否可复用")
    description: Optional[str] = Field(None, description="详细描述")
