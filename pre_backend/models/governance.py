from sqlalchemy import Column, Integer, String, JSON, Boolean
from models.base import BaseModel

class CapabilityTemplate(BaseModel):
    """
    权限能力模版（防止 Capability Matrix 爆炸）
    """
    __tablename__ = "capability_templates"

    name = Column(String(100), nullable=False, comment="模版名称")
    code = Column(String(50), unique=True, index=True, nullable=False, comment="模版编码: preview/standard/source")
    
    # 核心能力集：{"view": true, "download": false, "share": true, ...}
    capabilities = Column(JSON, nullable=False, comment="预设能力组合")
    
    is_default = Column(Boolean, default=False, comment="是否为默认模版")
    description = Column(String(255), nullable=True)
