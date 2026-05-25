"""
客户标签模型
用于记录客户的需求标签（如"详情页设计"、"3D建模"等）
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text, DateTime
from datetime import datetime
from models.base import BaseModel


class CustomerTag(BaseModel):
    """客户标签模型"""
    __tablename__ = "customer_tags"

    # 基本信息
    name = Column(String(100), nullable=False, comment="标签名称（如：详情页设计、3D建模等）")
    description = Column(Text, nullable=True, comment="标签描述")
    color = Column(String(20), nullable=True, comment="标签颜色标识（用于前端展示）")
    
    # 类别信息
    category = Column(String(50), nullable=True, 
                     comment="标签类别（service/skill/platform/other）")
    
    # 关联信息
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), 
                       nullable=True, comment="创建人ID")
    
    # 状态
    is_active = Column(Boolean, default=True, comment="是否启用")
    
    # 统计
    usage_count = Column(Integer, default=0, comment="被使用的次数")
    
    class Config:
        orm_mode = True


class CustomerTagAssociation(BaseModel):
    """客户标签关联表
    记录客户和标签的多对多关系
    """
    __tablename__ = "customer_tag_associations"

    # 外键关联
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), 
                        nullable=False, comment="客户ID")
    tag_id = Column(Integer, ForeignKey("customer_tags.id", ondelete="CASCADE"), 
                   nullable=False, comment="标签ID")
    
    # 关联信息
    assigned_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), 
                        nullable=True, comment="分配人ID")
    assigned_time = Column(DateTime, default=datetime.utcnow, comment="分配时间")
    
    # 备注
    remark = Column(Text, nullable=True, comment="分配备注")
    
    class Config:
        orm_mode = True
