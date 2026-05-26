from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float, JSON, Text, Index
from models.base import BaseModel
from datetime import datetime


class Task(BaseModel):
    """
    任务管理模型
    - 拆分自项目，绑定到任务分类
    - 支持多设计师协作（多角色）
    - 包含电商参数支持
    - 进度和状态追踪
    """
    __tablename__ = "tasks"

    # 关联字段
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"),
                        nullable=False, comment="项目ID")
    category_id = Column(Integer, ForeignKey("task_categories.id", ondelete="SET NULL"),
                         nullable=True, comment="任务分类ID")
    designer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"),
                         nullable=True, comment="主设计师ID")

    # 基本信息
    name = Column(String(255), nullable=False, comment="任务名称")
    description = Column(String(1000), nullable=True, comment="任务描述")

    # 多角色协作
    role_ids = Column(JSON, nullable=True, comment="参与角色ID列表")

    # 进度和主状态（唯一主状态机，避免状态爆炸）
    progress = Column(Float, default=0, nullable=False, comment="完成进度（0-100）")
    status = Column(String(50), default="待开始", nullable=False,
                    comment="主状态: 待开始/设计中/内审中/客户确认/逾期处理中/已完成/已归档/已暂停")
    
    # 异常流记录（非主状态）
    blocked_reason = Column(String(255), nullable=True, comment="阻塞原因")
    blocked_at = Column(DateTime, nullable=True)
    
    # 商业级锁：最终交付锁定
    is_locked = Column(Boolean, default=False, comment="物理锁定标记")
    locked_at = Column(DateTime, nullable=True)
    
    # 交付存证（法律闭环）
    review_deadline = Column(DateTime, nullable=True, comment="SLA 截止时间")
    finalized_at = Column(DateTime, nullable=True, comment="终稿确认点")
    delivery_snapshot_id = Column(Integer, nullable=True)
    
    # 内部内审 (QC) 环节
    qc_status = Column(String(20), default="pending", comment="内审状态（pending/approved/rejected）")
    qc_feedback = Column(Text, nullable=True, comment="内审意见")

    # 绩效与提成
    complexity_score = Column(Float, default=1.0, comment="任务难度系数(0.5-3.0)")
    commission_base = Column(Float, default=0.0, comment="基础提成金额")

    # 电商参数
    ecommerce_params = Column(JSON, nullable=True, comment="电商参数（平台/尺寸/分辨率等）")

    # 时间追踪
    deadline = Column(DateTime, nullable=True, comment="任务截止时间")
    start_time = Column(DateTime, nullable=True, comment="任务开始时间")
    end_time = Column(DateTime, nullable=True, comment="任务完成时间")

    # 备注和标记
    remark = Column(String(500), nullable=True, comment="任务备注")
    priority = Column(String(20), default="中", nullable=False,
                      comment="优先级（低/中/高/紧急）")

    is_active = Column(Boolean, default=True, nullable=False, comment="是否激活")

    # 售后风控
    revision_count = Column(Integer, default=0, nullable=False, comment="当前改稿总次数")
    revision_round = Column(Integer, default=1, nullable=False, comment="当前所处的改稿轮次(如第3轮修改)")
    max_revisions = Column(Integer, default=3, nullable=False, comment="最大免费改稿次数")

    # 商业级增强
    ext_data = Column(JSON, nullable=True, comment="自定义扩展数据")
    delivery_snapshot_id = Column(Integer, nullable=True, comment="最终交付锁定时的全局审计快照ID")

    # 复合索引优化
    __table_args__ = (
        Index("idx_task_org_deleted_status_designer", "org_id", "is_deleted", "status", "designer_id"),
    )

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name}, project_id={self.project_id}, status={self.status})>"
