from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from models.base import BaseModel
from datetime import datetime


class AfterSalesTicket(BaseModel):
    """
    售后工单/纠纷记录
    """
    __tablename__ = "after_sales_tickets"

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, comment="项目ID")
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True, comment="关联任务ID")
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="SET NULL"), nullable=True, comment="关联客户ID")
    
    type = Column(String(50), nullable=False, comment="售后类型（纠纷/改稿申请/故障申报）")
    title = Column(String(255), nullable=False, comment="标题")
    description = Column(Text, nullable=False, comment="描述/异议内容")
    
    status = Column(String(20), default="open", comment="状态（open/processing/resolved/closed）")
    priority = Column(String(20), default="normal", comment="优先级（low/normal/high/urgent）")
    
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="发起人ID")
    resolver_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="处理人ID")
    
    resolution = Column(Text, nullable=True, comment="处理结果/方案")
    closed_at = Column(DateTime, nullable=True, comment="关闭时间")


class RevisionLog(BaseModel):
    """
    改稿详细日志
    用于追踪任务的每一次微调，作为售后维权的凭证
    """
    __tablename__ = "revision_logs"

    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, comment="任务ID")
    revision_no = Column(Integer, nullable=False, comment="改稿版本号")
    
    description = Column(Text, nullable=False, comment="改稿需求描述")
    is_paid = Column(Text, default="false", comment="是否为付费改稿") # 使用 String 存储便于扩展
    
    designer_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="执行设计师ID")
    submit_time = Column(DateTime, default=datetime.utcnow, comment="需求提交时间")
    finish_time = Column(DateTime, nullable=True, comment="完成时间")
    
    feedback = Column(Text, nullable=True, comment="客户反馈")
