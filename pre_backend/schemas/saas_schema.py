from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============= Async Job =============
class AsyncJobRead(BaseModel):
    id: int
    task_name: str
    status: str
    progress: int
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_by: Optional[int] = None
    create_time: datetime
    update_time: datetime
    model_config = ConfigDict(from_attributes=True)


# ============= Webhook =============
class WebhookCreate(BaseModel):
    name: str = Field(..., description="Webhook 名称")
    url: str = Field(..., description="回调 URL")
    events: List[str] = Field(..., description="订阅的事件列表")
    secret: Optional[str] = Field(None, description="签名密钥")

class WebhookRead(BaseModel):
    id: int
    name: str
    url: str
    events: List[str]
    is_active: bool
    create_time: datetime
    model_config = ConfigDict(from_attributes=True)


class WebhookLogRead(BaseModel):
    id: int
    webhook_id: int
    event: str
    payload: Dict[str, Any]
    status: str
    response_code: Optional[int]
    error: Optional[str]
    create_time: datetime
    model_config = ConfigDict(from_attributes=True)


# ============= Search =============
class GlobalSearchResult(BaseModel):
    type: str = Field(..., description="结果类型（project/task/customer/material/file）")
    id: int = Field(..., description="对象ID")
    title: str = Field(..., description="标题/名称")
    subtitle: Optional[str] = Field(None, description="副标题/描述")
    url: Optional[str] = Field(None, description="直接访问链接或前端路由")
    match_score: Optional[float] = Field(None, description="匹配度得分")
