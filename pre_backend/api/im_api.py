from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from database.db import get_db
from models.user import User
from config.auth import get_current_user
from crud.im_crud import chat_session_crud, chat_message_crud
from schemas.im_schema import (
    ChatSessionRead, ChatSessionCreate, 
    ChatMessageRead, ChatMessageCreate
)

router = APIRouter()

# ============================================================
# 会话管理
# ============================================================

@router.post("/sessions", response_model=ChatSessionRead, summary="创建会话", description="发起新的私聊或群聊会话。")
def create_session(
    session_in: ChatSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建聊天会话"""
    return chat_session_crud.create_with_members(db, session_in, current_user.id)


@router.get("/sessions/me", response_model=List[ChatSessionRead], summary="获取我的会话", description="获取当前用户参与的所有活跃聊天会话。")
def list_my_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取个人会话列表"""
    return chat_session_crud.get_user_sessions(db, current_user.id)


# ============================================================
# 消息管理
# ============================================================

@router.post("/messages", response_model=ChatMessageRead, summary="发送消息", description="向指定会话发送文本、图片或文件消息。")
def send_message(
    msg_in: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """发送消息"""
    return chat_message_crud.send_message(db, msg_in, current_user.id)


@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageRead], summary="获取聊天记录", description="分页查询特定会话的历史消息记录。")
def list_session_messages(
    session_id: int = Path(..., description="会话ID"),
    skip: int = Query(0, description="跳过数"),
    limit: int = Query(50, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """查询会话消息历史"""
    return chat_message_crud.get_session_messages(db, session_id, skip, limit)
