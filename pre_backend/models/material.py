from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from models.base import BaseModel
from datetime import datetime


class Material(BaseModel):
    """
    素材库管理模型
    - 可复用的设计资源
    - 支持项目关联
    - 跟踪复用次数
    """
    __tablename__ = "materials"

    # 基本信息
    name = Column(String(255), nullable=False, comment="素材名称")
    type = Column(String(50), nullable=False, comment="素材类型（字体/icon/配色/模板等）")
    category = Column(String(100), nullable=True, comment="素材分类")
    description = Column(String(500), nullable=True, comment="素材描述")

    # 存储信息
    url = Column(String(500), nullable=False, comment="素材存储路径/URL")
    file_format = Column(String(20), nullable=True, comment="文件格式")
    size = Column(Integer, nullable=True, comment="文件大小（KB）")

    # 上传者
    uploader_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"),
                         nullable=True, comment="上传者ID")

    # 关联项目和任务
    project_ids = Column(JSON, nullable=True, comment="关联的项目ID列表")
    task_ids = Column(JSON, nullable=True, comment="关联的任务ID列表")

    # 复用管理
    is_reusable = Column(Boolean, default=True, nullable=False, comment="是否可复用")
    reuse_count = Column(Integer, default=0, nullable=False, comment="复用次数")
    tags = Column(JSON, nullable=True, comment="标签列表")

    # 时间追踪
    create_time = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, 
                        nullable=False, comment="更新时间")

    is_active = Column(Boolean, default=True, nullable=False, comment="是否激活")

    def __repr__(self):
        return f"<Material(id={self.id}, name={self.name}, type={self.type})>"
