from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from models.base import BaseModel
from datetime import datetime

class Approval(BaseModel):
    """
    通用审批流模型
    """
    __tablename__ = "approvals"

    title = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False, comment="审批类型: vacation/expense/project")
    
    applicant_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    content = Column(JSON, nullable=True, comment="审批详情内容")
    status = Column(String(20), default="pending", comment="pending/approved/rejected")
    
    remark = Column(String(500), nullable=True)


class UnlockRequest(BaseModel):
    """
    解锁申请（Side Workflow，不干扰主状态机）
    """
    __tablename__ = "unlock_requests"

    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    reason = Column(Text, nullable=False, comment="申请解锁的具体原因")
    
    # 多级审批
    supervisor_approved = Column(Integer, ForeignKey("users.id"), nullable=True, comment="主管审批人")
    finance_approved = Column(Integer, ForeignKey("users.id"), nullable=True, comment="财务审批人")
    admin_approved = Column(Integer, ForeignKey("users.id"), nullable=True, comment="管理员审批人")
    
    # 工业级增强：风险分级
    # risk_level: low(常规修改), medium(关键变动), high(交付物重置), legal(已开票/涉及法律风险)
    risk_level = Column(String(20), default="low", comment="解锁风险等级")
    
    status = Column(String(20), default="pending", comment="pending/approved/rejected")
    
    # 法律/财务备注
    legal_notes = Column(Text, nullable=True, comment="合规性备注")
