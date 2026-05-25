from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class AttendanceRecordBase(BaseModel):
    user_id: int
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    date: Optional[datetime] = None
    status: str = "normal"
    location: Optional[str] = None
    device_info: Optional[str] = None
    remark: Optional[str] = None


class AttendanceRecordCreate(BaseModel):
    location: Optional[str] = None
    device_info: Optional[str] = None
    remark: Optional[str] = None


class AttendanceRecordRead(AttendanceRecordBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TimesheetBase(BaseModel):
    task_id: Optional[int] = None
    project_id: Optional[int] = None
    duration: int = Field(..., description="时长（分钟）")
    work_date: Optional[datetime] = None
    description: str = Field(..., description="工作内容")
    status: str = "pending"


class TimesheetCreate(TimesheetBase):
    pass


class TimesheetRead(TimesheetBase):
    id: int
    user_id: int
    create_time: datetime
    model_config = ConfigDict(from_attributes=True)


class PerformanceReviewRead(BaseModel):
    id: int
    user_id: int
    period: str
    score: int
    rating: Optional[str] = None
    output_count: int
    revision_rate: float
    on_time_rate: float
    bonus_amount: int
    summary: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
