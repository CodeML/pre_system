from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from models.base import BaseModel
from datetime import datetime


class Notification(BaseModel):
    """
    消息通知模型
    - 支持多种通知类型（任务分配、客户确认、超期提醒等）
    - 支持已读/未读状态
    - 跟踪发送者和接收者
    """
    __tablename__ = "notifications"

    # 关联字段
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                       nullable=True, comment="发送者ID（系统自动为NULL）")
    recipient_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                          nullable=False, comment="接收者ID")
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"),
                     nullable=True, comment="关联任务ID")
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="SET NULL"),
                        nullable=True, comment="关联项目ID")

    # 通知内容
    type = Column(String(50), nullable=False, comment="通知类型（task_assigned/task_completed/overdue/customer_confirmed等）")
    title = Column(String(255), nullable=False, comment="通知标题")
    content = Column(Text, nullable=False, comment="通知内容")
    action_url = Column(String(500), nullable=True, comment="操作链接")

    # 状态
    is_read = Column(Boolean, default=False, nullable=False, comment="是否已读")
    read_time = Column(DateTime, nullable=True, comment="阅读时间")

    # 优先级
    priority = Column(String(20), default="normal", nullable=False, comment="优先级（low/normal/high/urgent）")

    # 时间追踪
    create_time = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否激活")

    def __repr__(self):
        return f"<Notification(id={self.id}, type={self.type}, recipient_id={self.recipient_id}, is_read={self.is_read})>"


class NotificationSetting(BaseModel):
    """
    用户通知偏好设置
    """
    __tablename__ = "notification_settings"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # 订阅开关
    enable_email = Column(Boolean, default=True)
    enable_push = Column(Boolean, default=True)
    
    # 屏蔽列表（逗号分隔的类型）
    muted_types = Column(String(500), nullable=True, comment="屏蔽的消息类型")


class NotificationTemplate(BaseModel):
    """
    通知话术模版
    """
    __tablename__ = "notification_templates"

    code = Column(String(50), unique=True, index=True, nullable=False, comment="模版唯一编码")
    title_tpl = Column(String(255), nullable=False, comment="标题模版")
    content_tpl = Column(Text, nullable=False, comment="内容模版")
    
    type = Column(String(20), comment="模版分类")
    is_active = Column(Boolean, default=True)
