from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 租户隔离
    org_id = Column(Integer, default=1, index=True, comment="所属组织/租户ID")
    
    # 软删除支持
    is_deleted = Column(Boolean, default=False, index=True, comment="是否已删除")
    delete_time = Column(DateTime, nullable=True, comment="删除时间")
