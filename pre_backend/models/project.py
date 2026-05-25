from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from models.base import BaseModel
from datetime import datetime


class Project(BaseModel):
    """
    项目管理模型
    - 关联客户和设计师
    - 支持多个项目类型（电商详情页/3D建模/摄影）
    - 按电商平台区分
    - 支持多个素材库ID
    """
    __tablename__ = "projects"

    name = Column(String(255), nullable=False, comment="项目名称")
    
    # 关联字段
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), 
                         nullable=False, comment="客户ID")
    main_designer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"),
                              nullable=True, comment="主设计师ID")
    assist_designer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"),
                                nullable=True, comment="辅助设计师ID")
    
    # 项目信息
    type = Column(String(50), nullable=False, comment="项目类型（电商详情页/3D建模/摄影）")
    ecommerce_platform = Column(String(50), nullable=True, 
                                comment="电商平台（淘宝/抖音/小红书/Amazon等）")
    
    # 素材和配置
    material_ids = Column(JSON, nullable=True, comment="关联的素材库ID列表")
    params = Column(JSON, nullable=True, comment="项目扩展参数")
    
    # 状态和时间
    status = Column(String(50), default="待启动", nullable=False, 
                    comment="项目状态（待启动/设计中/待确认/已交付/已完结）")
    start_time = Column(DateTime, nullable=True, comment="项目开始时间")
    end_time = Column(DateTime, nullable=True, comment="项目结束时间")
    
    # 备注
    remark = Column(String(500), nullable=True, comment="项目备注")
    
    is_active = Column(Boolean, default=True, nullable=False, comment="是否激活")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name}, customer_id={self.customer_id})>"
