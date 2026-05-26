from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from models.base import BaseModel
from datetime import datetime


class CustomerFollowUp(BaseModel):
    """
    客户跟进记录
    """
    __tablename__ = "customer_follow_ups"

    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, comment="客户ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="跟进人ID")
    
    content = Column(Text, nullable=False, comment="跟进内容")
    contact_type = Column(String(50), comment="联系方式（电话/微信/面谈等）")
    
    next_follow_up_time = Column(DateTime, nullable=True, comment="下次跟进时间计划")
    is_important = Column(Boolean, default=False)


class ProjectMilestone(BaseModel):
    """
    项目里程碑
    """
    __tablename__ = "project_milestones"

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, comment="项目ID")
    name = Column(String(100), nullable=False, comment="里程碑名称（初稿/定稿等）")
    
    due_date = Column(DateTime, nullable=True, comment="计划达成日期")
    completed_at = Column(DateTime, nullable=True, comment="实际达成时间")
    
    status = Column(String(20), default="pending", comment="状态（pending/completed/missed）")
    remark = Column(String(500), nullable=True)


class TaskReminder(BaseModel):
    """
    任务提醒设置
    """
    __tablename__ = "task_reminders"

    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, comment="任务ID")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="被提醒人ID")
    
    remind_time = Column(DateTime, nullable=False, comment="提醒触发时间")
    message = Column(String(255), nullable=True, comment="提醒文案")
    
    is_sent = Column(Boolean, default=False, comment="是否已发送")
