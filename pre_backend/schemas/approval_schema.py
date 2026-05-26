from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class ApprovalCreate(BaseModel):
    type: str = Field(..., description="审批类型（quotation/expense/leave等）")
    target_id: int = Field(..., description="关联业务对象ID")
    approver_id: Optional[int] = Field(None, description="指定审批人ID")
    priority: str = Field("normal", description="优先级")
    content: Optional[str] = Field(None, description="申请说明")


class ApprovalRead(BaseModel):
    id: int
    type: str
    target_id: int
    requester_id: int
    approver_id: Optional[int]
    status: str
    content: Optional[str]
    reason: Optional[str]
    create_time: datetime
    finish_time: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)
