"""
通知 Pydantic 模式
"""
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class NotificationCreate(BaseModel):
    """创建通知"""
    recipient_id: int = Field(..., description="接收人用户ID")
    type: str = Field(..., description="通知类型")
    title: str = Field(..., description="标题")
    content: str = Field(..., description="正文内容")
    task_id: Optional[int] = Field(None, description="关联任务ID")
    project_id: Optional[int] = Field(None, description="关联项目ID")
    priority: str = Field("normal", description="优先级")
    action_url: Optional[str] = Field(None, description="点击跳转链接")


class NotificationRead(BaseModel):
    """读取通知"""
    id: int = Field(..., description="通知ID")
    recipient_id: int = Field(..., description="接收人用户ID")
    type: str = Field(..., description="类型")
    title: str = Field(..., description="标题")
    content: str = Field(..., description="内容")
    is_read: bool = Field(..., description="是否已读")
    priority: str = Field(..., description="优先级")
    create_time: datetime = Field(..., description="创建时间")
    read_time: Optional[datetime] = Field(None, description="阅读时间")
    task_id: Optional[int] = Field(None, description="任务ID")
    project_id: Optional[int] = Field(None, description="项目ID")
    action_url: Optional[str] = Field(None, description="跳转链接")

    model_config = ConfigDict(from_attributes=True)


class NotificationUpdate(BaseModel):
    """更新通知"""
    is_read: Optional[bool] = Field(None, description="标记已读/未读")
    priority: Optional[str] = Field(None, description="修改优先级")


class NotificationStatistics(BaseModel):
    """通知统计"""
    total: int = Field(..., description="总数")
    unread: int = Field(..., description="未读数")
    read: int = Field(..., description="已读数")
    by_type: dict = Field(..., description="按类型分布")
    by_priority: dict = Field(..., description="按优先级分布")
