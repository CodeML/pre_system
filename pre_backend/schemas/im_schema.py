from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class ChatSessionBase(BaseModel):
    name: Optional[str] = None
    type: str = "private"
    project_id: Optional[int] = None


class ChatSessionCreate(ChatSessionBase):
    member_ids: List[int]


class ChatSessionRead(ChatSessionBase):
    id: int
    last_message_at: datetime
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class ChatMessageBase(BaseModel):
    session_id: int
    content: str
    msg_type: str = "text"
    file_url: Optional[str] = None
    reply_to_id: Optional[int] = None


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageRead(ChatMessageBase):
    id: int
    sender_id: int
    is_read: bool
    create_time: datetime
    model_config = ConfigDict(from_attributes=True)
