from sqlalchemy import Column, Integer, ForeignKey, String, Text, Boolean, DateTime
from models.base import BaseModel
from datetime import datetime


class TaskComment(BaseModel):
    __tablename__ = "task_comments"

    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True, comment="关联任务ID")
    author_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="作者用户ID")
    content = Column(Text, nullable=False, comment="评论内容")
    parent_id = Column(Integer, ForeignKey("task_comments.id", ondelete="CASCADE"), nullable=True, comment="父评论ID（回复）")
    is_public = Column(Boolean, default=True, comment="是否对客户可见")
    is_active = Column(Boolean, default=True, comment="是否激活（软删除）")

    def __repr__(self):
        return f"<TaskComment id={self.id} task_id={self.task_id} author_id={self.author_id}>"
