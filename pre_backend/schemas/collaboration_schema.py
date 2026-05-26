from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime


class CommentCreate(BaseModel):
    target_type: str = Field(..., description="对象类型(project/task/file/revision)")
    target_id: int = Field(..., description="对象ID")
    content: str = Field(..., description="正文")
    
    # 画布批注
    pos_x: Optional[float] = None
    pos_y: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    
    page_index: Optional[int] = 0
    artboard_id: Optional[str] = None
    annotation_type: Optional[str] = "point"
    annotation_status: Optional[str] = "open"
    
    parent_id: Optional[int] = None
    is_internal: bool = False


class CommentRead(BaseModel):
    id: int
    target_type: str
    target_id: int
    content: str
    author_id: int
    
    pos_x: Optional[float]
    pos_y: Optional[float]
    page_index: int
    annotation_type: str
    annotation_status: str
    
    is_resolved: bool
    create_time: datetime
    
    model_config = ConfigDict(from_attributes=True)
