from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from models.base import BaseModel
from datetime import datetime


class File(BaseModel):
    """
    设计文件管理模型
    - 关联任务和素材库
    - 支持版本管理
    - 跟踪上传者和确认者
    """
    __tablename__ = "files"

    # 关联字段
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"),
                     nullable=False, comment="任务ID")
    material_id = Column(Integer, ForeignKey("materials.id", ondelete="SET NULL"),
                         nullable=True, comment="关联素材ID（若复用素材）")
    uploader_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"),
                         nullable=True, comment="上传者ID")

    # 基本信息
    name = Column(String(255), nullable=False, comment="文件名称")
    description = Column(String(500), nullable=True, comment="文件描述")

    # 文件信息
    url = Column(String(500), nullable=False, comment="文件存储路径/URL")
    file_type = Column(String(50), nullable=False, comment="文件类型（设计稿/3D模型/摄影图/视频等）")
    file_format = Column(String(20), nullable=True, comment="文件格式（psd/ai/jpg等）")
    size = Column(Float, nullable=True, comment="文件大小（MB）")
    
    # 云存储信息
    storage_type = Column(String(50), default="local", nullable=False, comment="存储类型 (local/s3/oss等)")
    storage_key = Column(String(500), nullable=True, comment="云存储的文件 key")

    # 版本管理
    version = Column(String(50), default="v1", nullable=False, comment="版本号（如 v1, v2, v1_draft等）")
    is_latest = Column(Boolean, default=True, nullable=False, comment="是否最新版本")

    # 确认流程
    is_confirm = Column(Boolean, default=False, nullable=False, comment="是否已确认")
    confirm_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"),
                             nullable=True, comment="确认者ID")
    confirm_time = Column(DateTime, nullable=True, comment="确认时间")
    confirm_remark = Column(String(500), nullable=True, comment="确认备注")

    # 分享链接
    share_token = Column(String(100), nullable=True, comment="分享令牌")
    share_expiry = Column(DateTime, nullable=True, comment="分享链接过期时间")
    is_shared = Column(Boolean, default=False, nullable=False, comment="是否已分享")

    # 时间追踪
    upload_time = Column(DateTime, default=datetime.utcnow, nullable=False, comment="上传时间")

    is_active = Column(Boolean, default=True, nullable=False, comment="是否激活")

    def __repr__(self):
        return f"<File(id={self.id}, name={self.name}, version={self.version}, task_id={self.task_id})>"
