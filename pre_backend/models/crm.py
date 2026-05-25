from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean
from models.base import BaseModel
from datetime import datetime


class SalesLead(BaseModel):
    """
    销售线索/意向客户
    """
    __tablename__ = "sales_leads"

    name = Column(String(255), nullable=False, comment="联系人/线索名称")
    phone = Column(String(50), nullable=True, comment="联系电话")
    source = Column(String(50), comment="线索来源（转介绍/平台广告/主动咨询）")
    
    status = Column(String(20), default="new", comment="状态（new/following/converted/closed）")
    priority = Column(String(20), default="normal", comment="优先级")
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="负责人ID")
    last_follow_up = Column(DateTime, nullable=True, comment="最后跟进时间")
    next_follow_up = Column(DateTime, nullable=True, comment="下次跟进时间")
    
    remark = Column(Text, nullable=True, comment="备注/意向描述")


class DesignPackage(BaseModel):
    """
    设计套餐/服务产品
    """
    __tablename__ = "design_packages"

    name = Column(String(255), nullable=False, comment="套餐名称")
    description = Column(Text, nullable=True, comment="套餐介绍")
    price = Column(Float, nullable=False, comment="价格")
    
    unit = Column(String(20), default="套", comment="计价单位")
    include_revisions = Column(Integer, default=3, comment="包含改稿次数")
    
    is_active = Column(Boolean, default=True, comment="是否上架")
    category = Column(String(50), comment="业务分类")


class CaseWork(BaseModel):
    """
    案例作品集
    """
    __tablename__ = "case_works"

    title = Column(String(255), nullable=False, comment="作品标题")
    description = Column(Text, nullable=True, comment="设计说明")
    
    cover_url = Column(String(500), nullable=False, comment="封面图地址")
    content_urls = Column(Text, nullable=True, comment="作品详情图(逗号分隔或JSON)")
    
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, comment="关联项目ID")
    category = Column(String(50), comment="分类（主图/详情页/3D等）")
    
    tags = Column(String(255), nullable=True, comment="作品标签")
    is_public = Column(Boolean, default=True, comment="是否对外公开")
