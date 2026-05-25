from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text, JSON
from models.base import BaseModel


class TaskCategory(BaseModel):
    __tablename__ = "task_categories"
    
    parent_id = Column(Integer, ForeignKey("task_categories.id", ondelete="SET NULL"), nullable=True, comment="父分类ID（多级分类）")
    name = Column(String(100), index=True, comment="分类名称：设计/3D建模/摄影/平面等")
    role_ids = Column(JSON, nullable=True, comment="可操作此分类的角色ID列表（JSON数组）")
    is_ecommerce = Column(Boolean, default=False, comment="是否为电商设计分类")
    params = Column(JSON, nullable=True, comment="分类参数（JSON格式，用于存储自定义配置）")
    description = Column(Text, nullable=True, comment="分类描述")
    is_active = Column(Boolean, default=True, comment="是否启用")
