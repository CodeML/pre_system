from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float, JSON
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

    # 进度和状态
    progress = Column(Float, default=0, nullable=False, comment="完成进度（0-100）")
    status = Column(String(50), default="待开始", nullable=False,
                    comment="任务状态（待开始/进行中/待确认/已完成）")

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
    revision_count = Column(Integer, default=0, nullable=False, comment="当前改稿次数")
    max_revisions = Column(Integer, default=3, nullable=False, comment="最大免费改稿次数")

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name}, project_id={self.project_id}, status={self.status})>"
