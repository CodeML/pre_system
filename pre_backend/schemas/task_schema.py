from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TaskCreate(BaseModel):
    """创建任务请求"""
    project_id: int = Field(..., description="项目ID")
    category_id: int = Field(..., description="任务分类ID")
    name: str = Field(..., min_length=1, max_length=255, description="任务名称")
    designer_id: Optional[int] = Field(None, description="设计师ID")
    role_ids: Optional[List[int]] = Field(None, description="参与角色ID列表")
    description: Optional[str] = Field(None, max_length=1000, description="任务描述")
    progress: Optional[float] = Field(0, ge=0, le=100, description="初始进度")
    status: Optional[str] = Field("待开始", description="任务状态")
    ecommerce_params: Optional[dict] = Field(None, description="电商参数")
    deadline: Optional[datetime] = Field(None, description="截止时间")
    priority: Optional[str] = Field("中", description="优先级（低/中/高/紧急）")
    remark: Optional[str] = Field(None, max_length=500, description="备注")


class TaskUpdate(BaseModel):
    """更新任务请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="任务名称")
    description: Optional[str] = Field(None, max_length=1000, description="任务描述")
    designer_id: Optional[int] = Field(None, description="主设计师ID")
    status: Optional[str] = Field(None, description="任务状态")
    priority: Optional[str] = Field(None, description="优先级")
    deadline: Optional[datetime] = Field(None, description="截止时间")
    remark: Optional[str] = Field(None, max_length=500, description="备注")


class TaskProgressUpdate(BaseModel):
    """任务进度更新"""
    progress: float = Field(..., ge=0, le=100, description="完成进度（0-100）")


class TaskRead(BaseModel):
    """任务读取响应"""
    id: int = Field(..., description="任务ID")
    project_id: int = Field(..., description="所属项目ID")
    category_id: Optional[int] = Field(None, description="所属分类ID")
    name: str = Field(..., description="任务名称")
    designer_id: Optional[int] = Field(None, description="主设计师ID")
    role_ids: Optional[List[int]] = Field(None, description="参与角色ID列表")
    description: Optional[str] = Field(None, description="任务描述")
    progress: float = Field(..., description="任务进度(0-100)")
    status: str = Field(..., description="任务状态")
    ecommerce_params: Optional[dict] = Field(None, description="电商特定参数")
    deadline: Optional[datetime] = Field(None, description="截止日期")
    priority: str = Field(..., description="优先级")
    start_time: Optional[datetime] = Field(None, description="实际开始时间")
    end_time: Optional[datetime] = Field(None, description="实际完成时间")
    remark: Optional[str] = Field(None, description="备注")
    is_active: bool = Field(True, description="任务是否活跃")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="最后更新时间")

    class Config:
        from_attributes = True


class TaskListRead(BaseModel):
    """任务列表响应"""
    id: int = Field(..., description="任务ID")
    project_id: int = Field(..., description="所属项目ID")
    category_id: Optional[int] = Field(None, description="所属分类ID")
    name: str = Field(..., description="任务名称")
    designer_id: Optional[int] = Field(None, description="主设计师ID")
    status: str = Field(..., description="任务状态")
    progress: float = Field(..., description="任务进度")
    priority: str = Field(..., description="优先级")
    deadline: Optional[datetime] = Field(None, description="截止日期")
    create_time: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True


class ProjectProgressRead(BaseModel):
    """项目进度统计"""
    total: int = Field(..., description="任务总数")
    completed: int = Field(..., description="已完成数")
    in_progress: int = Field(..., description="进行中数")
    pending: int = Field(..., description="待开始数")
    average_progress: float = Field(..., description="平均进度(0-100)")
    completion_rate: str = Field(..., description="完成率百分比字符串")
