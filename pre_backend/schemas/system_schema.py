from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class TrashRecordRead(BaseModel):
    id: int
    original_table: str = Field(..., description="原始表名")
    original_id: int = Field(..., description="原始ID")
    deleted_by: Optional[int] = None
    deleted_at: datetime
    data: dict = Field(..., description="数据快照")
    
    model_config = ConfigDict(from_attributes=True)


class DraftBase(BaseModel):
    type: str = Field(..., description="类型")
    title: Optional[str] = None
    data: dict = Field(..., description="内容JSON")


class DraftCreate(DraftBase):
    pass


class DraftRead(DraftBase):
    id: int
    user_id: int
    last_saved_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
