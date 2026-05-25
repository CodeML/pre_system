from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskCommentCreate(BaseModel):
    content: str = Field(..., description="评论内容")
    parent_id: Optional[int] = Field(None, description="父评论ID（用于回复）")
    is_public: bool = Field(True, description="是否公开可见")


class TaskCommentRead(BaseModel):
    id: int = Field(..., description="评论ID")
    task_id: int = Field(..., description="关联任务ID")
    author_id: Optional[int] = Field(None, description="作者ID")
    content: str = Field(..., description="内容")
    parent_id: Optional[int] = Field(None, description="父评论ID")
    is_public: bool = Field(True, description="是否公开")
    create_time: Optional[datetime] = Field(None, description="发表时间")

    class Config:
        from_attributes = True
