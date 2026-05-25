from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class AfterSalesTicketBase(BaseModel):
    project_id: int
    task_id: Optional[int] = None
    customer_id: Optional[int] = None
    type: str = Field(..., description="售后类型")
    title: str = Field(..., description="标题")
    description: str = Field(..., description="详情")
    status: str = "open"
    priority: str = "normal"


class AfterSalesTicketCreate(AfterSalesTicketBase):
    pass


class AfterSalesTicketRead(AfterSalesTicketBase):
    id: int
    creator_id: Optional[int] = None
    resolver_id: Optional[int] = None
    resolution: Optional[str] = None
    create_time: datetime
    closed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class RevisionLogBase(BaseModel):
    task_id: int
    revision_no: int
    description: str
    is_paid: str = "false"
    designer_id: Optional[int] = None


class RevisionLogCreate(RevisionLogBase):
    pass


class RevisionLogRead(RevisionLogBase):
    id: int
    submit_time: datetime
    finish_time: Optional[datetime] = None
    feedback: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
