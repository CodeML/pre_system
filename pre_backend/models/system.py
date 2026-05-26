from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Boolean
from models.base import BaseModel
from datetime import datetime


class OperationLog(BaseModel):
    """
    全局操作日志
    用于审计、溯源和纠纷举证
    """
    __tablename__ = "operation_logs"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="操作人ID")
    module = Column(String(50), nullable=False, comment="所属模块（项目/任务/财务等）")
    action = Column(String(100), nullable=False, comment="操作动作（新增/编辑/删除/导出等）")
    
    target_id = Column(String(100), nullable=True, comment="操作对象ID（如项目ID、任务ID）")
    content = Column(Text, nullable=True, comment="操作详细内容/变动前后的差异JSON")
    
    ip_address = Column(String(50), nullable=True, comment="操作人IP")
    user_agent = Column(String(255), nullable=True, comment="操作设备信息")
    
    # 工业级增强：时间轴分层 (Timeline Layering)
    # visibility: business(客户可见), audit(内部可见), system(系统级)
    visibility = Column(String(20), default="audit", index=True, comment="可见性分层")

    status = Column(String(20), default="success", comment="操作状态（success/failed）")
    error_msg = Column(Text, nullable=True, comment="失败原因")


class TrashRecord(BaseModel):
    """
    统一回收站（多态模型）
    """
    __tablename__ = "trash_records"

    # 核心字段：记录来源
    target_type = Column(String(50), nullable=False, comment="业务对象类型（project/task/file）")
    target_id = Column(Integer, nullable=False, comment="原始ID")
    
    # 核心字段：数据快照
    snapshot = Column(JSON, nullable=False, comment="删除前的数据快照")
    
    # 审计
    deleted_by = Column(Integer, ForeignKey("users.id"), nullable=True, comment="执行删除的用户")
    reason = Column(String(255), nullable=True, comment="删除原因")
    
    # 状态：是否已恢复
    is_restored = Column(Boolean, default=False)
    restored_at = Column(DateTime, nullable=True)


class Draft(BaseModel):
    """
    草稿管理
    """
    __tablename__ = "drafts"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False, comment="草稿类型（project/task/quotation等）")
    
    title = Column(String(255), nullable=True)
    data = Column(JSON, nullable=False, comment="草稿内容JSON")
    
    last_saved_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
