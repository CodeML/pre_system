from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from database.db import get_db
from models.user import User
from models.collaboration import Comment
from config.auth import get_current_user
from schemas.collaboration_schema import CommentCreate, CommentRead
from datetime import datetime

router = APIRouter()

# ============================================================
# 协作讨论与批注 (Comment & Annotation)
# ============================================================

@router.post("/comments", response_model=CommentRead, summary="发表评论/批注", description="在项目、任务、文件上发表协作评论，支持画布坐标批注。")
def create_comment(
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_obj = Comment(**comment_in.model_dump(), author_id=current_user.id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/comments/{target_type}/{target_id}", response_model=List[CommentRead], summary="获取讨论流")
def list_comments(
    target_type: str = Path(..., description="对象类型"),
    target_id: int = Path(..., description="对象ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取指定业务对象的全量协作讨论流"""
    query = db.query(Comment).filter(
        Comment.target_type == target_type,
        Comment.target_id == target_id,
        Comment.is_deleted == False
    )
    
    # 客户只能看到非内部评论
    # 简单权限逻辑模拟
    if current_user.username.startswith("client"):
        query = query.filter(Comment.is_internal == False)
        
    return query.order_by(Comment.create_time.asc()).all()


@router.put("/comments/{comment_id}/status/{new_status}", summary="更新批注状态", description="修改批注的状态（open/resolved/ignored/reopened）。")
def update_annotation_status(
    comment_id: int = Path(...),
    new_status: str = Path(..., description="新状态"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新批注生命周期状态"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    valid_statuses = ["open", "resolved", "ignored", "reopened"]
    if new_status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"无效的状态，支持: {valid_statuses}")
        
    comment.annotation_status = new_status
    # 向下兼容
    if new_status == "resolved":
        comment.is_resolved = True
        
    db.commit()
    return {"message": f"批注状态已更新为 {new_status}"}
