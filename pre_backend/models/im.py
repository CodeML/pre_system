from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from models.base import BaseModel
from datetime import datetime


class ChatSession(BaseModel):
    """
    聊天会话
    """
    __tablename__ = "chat_sessions"

    name = Column(String(255), nullable=True, comment="会话名称（群聊用）")
    type = Column(String(20), default="private", comment="类型（private-私聊/group-群聊/project-项目组/client-客户沟通）")
    
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=True, comment="关联项目ID")
    last_message_at = Column(DateTime, default=datetime.utcnow, comment="最后消息时间")
    
    is_active = Column(Boolean, default=True, comment="是否活跃")


class ChatSessionMember(BaseModel):
    """
    会话成员关系
    """
    __tablename__ = "chat_session_members"

    session_id = Column(Integer, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    joined_at = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False, comment="是否为群管理员")
    mute_notifications = Column(Boolean, default=False, comment="是否免打扰")


class ChatMessage(BaseModel):
    """
    聊天消息
    """
    __tablename__ = "chat_messages"

    session_id = Column(Integer, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    content = Column(Text, nullable=False, comment="消息内容")
    msg_type = Column(String(20), default="text", comment="内容类型（text/image/file/system）")
    
    is_read = Column(Boolean, default=False)
    file_url = Column(String(500), nullable=True, comment="附件地址")
    
    # 引用/回复
    reply_to_id = Column(Integer, ForeignKey("chat_messages.id"), nullable=True)
