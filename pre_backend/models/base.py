from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
