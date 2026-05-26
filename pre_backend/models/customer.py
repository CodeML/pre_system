from sqlalchemy import Column, String, Integer, ForeignKey, Text, JSON, Index
from models.base import BaseModel


class Customer(BaseModel):
    __tablename__ = "customers"
    
    name = Column(String(100), index=True, comment="客户名称/公司名")
    contact = Column(String(50), nullable=True, comment="联系人")
    phone = Column(String(20), nullable=True, comment="联系电话")
    type = Column(String(50), default="individual", comment="客户类型：individual/company/brand")
    ecommerce_platform = Column(String(100), nullable=True, comment="电商平台：淘宝/抖音/小红书/Amazon等")
    remark = Column(Text, nullable=True, comment="备注信息")
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="创建人ID（设计总监）")
    
    # 商业级增强
    ext_data = Column(JSON, nullable=True, comment="扩展字段")

    # 复合索引优化
    __table_args__ = (
        Index("idx_customer_org_deleted", "org_id", "is_deleted"),
    )
