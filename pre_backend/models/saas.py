from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Boolean
from models.base import BaseModel
from datetime import datetime

class AsyncJob(BaseModel):
    """
    异步后台任务
    """
    __tablename__ = "async_jobs"

    task_name = Column(String(100), nullable=False, comment="任务名称（如：批量导入客户、分片合并）")
    status = Column(String(20), default="pending", comment="状态（pending/processing/completed/failed）")
    progress = Column(Integer, default=0, comment="进度百分比")
    
    result = Column(JSON, nullable=True, comment="成功时的返回数据")
    error = Column(Text, nullable=True, comment="失败时的错误堆栈")
    
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True, comment="触发任务的用户ID")


class Webhook(BaseModel):
    """
    Webhook 订阅
    """
    __tablename__ = "webhooks"

    name = Column(String(100), nullable=False, comment="Webhook 名称")
    url = Column(String(500), nullable=False, comment="回调 URL")
    events = Column(JSON, nullable=False, comment="订阅的事件列表（如：['task.completed', 'project.created']）")
    
    secret = Column(String(100), nullable=True, comment="签名密钥")
    is_active = Column(Boolean, default=True, comment="是否启用")


class WebhookLog(BaseModel):
    """
    Webhook 推送日志
    """
    __tablename__ = "webhook_logs"

    webhook_id = Column(Integer, ForeignKey("webhooks.id", ondelete="CASCADE"), nullable=False)
    event = Column(String(100), nullable=False, comment="触发事件")
    payload = Column(JSON, nullable=False, comment="推送的数据载荷")
    
    status = Column(String(20), nullable=False, comment="状态（success/failed）")
    response_code = Column(Integer, nullable=True, comment="外部系统响应码")
    error = Column(Text, nullable=True, comment="推送失败原因")


class EventRecord(BaseModel):
    """
    业务事件记录（可靠消息投递/最终一致性）
    """
    __tablename__ = "event_records"

    event_type = Column(String(100), nullable=False, comment="事件类型（如：order.paid, task.review_passed）")
    payload = Column(JSON, nullable=False, comment="事件数据载荷")
    
    status = Column(String(20), default="pending", comment="状态（pending/processed/failed）")
    retry_count = Column(Integer, default=0)
    
    trace_id = Column(String(100), nullable=True, comment="分布式链路追踪ID")
