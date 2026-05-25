from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProjectCreate(BaseModel):
    """创建项目请求"""
    name: str = Field(..., min_length=1, max_length=255, description="项目名称")
    customer_id: int = Field(..., description="客户ID")
    type: str = Field(..., description="项目类型（电商详情页/3D建模/摄影）")
    ecommerce_platform: Optional[str] = Field(None, description="电商平台")
    main_designer_id: Optional[int] = Field(None, description="主设计师ID")
    assist_designer_id: Optional[int] = Field(None, description="辅助设计师ID")
    material_ids: Optional[List[int]] = Field(None, description="素材ID列表")
    status: Optional[str] = Field("待启动", description="项目状态")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    remark: Optional[str] = Field(None, max_length=500, description="备注")


class ProjectUpdate(BaseModel):
    """更新项目请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="项目名称")
    type: Optional[str] = Field(None, description="项目类型")
    ecommerce_platform: Optional[str] = Field(None, description="电商平台")
    main_designer_id: Optional[int] = Field(None, description="主设计师ID")
    assist_designer_id: Optional[int] = Field(None, description="辅助设计师ID")
    status: Optional[str] = Field(None, description="项目状态")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    remark: Optional[str] = Field(None, max_length=500, description="备注")


class ProjectRead(BaseModel):
    """项目读取响应"""
    id: int = Field(..., description="项目ID")
    name: str = Field(..., description="项目名称")
    customer_id: int = Field(..., description="客户ID")
    type: str = Field(..., description="项目类型")
    ecommerce_platform: Optional[str] = Field(None, description="电商平台")
    main_designer_id: Optional[int] = Field(None, description="主设计师ID")
    assist_designer_id: Optional[int] = Field(None, description="辅助设计师ID")
    material_ids: Optional[List[int]] = Field(None, description="关联素材ID列表")
    status: str = Field(..., description="当前状态")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    remark: Optional[str] = Field(None, description="备注说明")
    is_active: bool = Field(True, description="是否活跃")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="最后更新时间")

    class Config:
        from_attributes = True


class ProjectListRead(BaseModel):
    """项目列表响应"""
    id: int = Field(..., description="项目ID")
    name: str = Field(..., description="项目名称")
    customer_id: int = Field(..., description="客户ID")
    type: str = Field(..., description="项目类型")
    ecommerce_platform: Optional[str] = Field(None, description="电商平台")
    status: str = Field(..., description="当前状态")
    main_designer_id: Optional[int] = Field(None, description="主设计师ID")
    assist_designer_id: Optional[int] = Field(None, description="辅助设计师ID")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="最后更新时间")

    class Config:
        from_attributes = True
