from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from database.db import get_db
from models.user import User
from config.auth import get_current_user
from crud.after_sales_crud import after_sales_ticket_crud, revision_log_crud
from schemas.after_sales_schema import (
    AfterSalesTicketRead, AfterSalesTicketCreate, RevisionLogRead, RevisionLogCreate
)

router = APIRouter()

# ============================================================
# 售后工单
# ============================================================

@router.post("/tickets", response_model=AfterSalesTicketRead, summary="创建售后工单", description="发起一个新的售后或投诉请求。")
def create_ticket(
    ticket_in: AfterSalesTicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建售后工单"""
    # 设置创建人
    db_obj = after_sales_ticket_crud.create(db, ticket_in)
    db_obj.creator_id = current_user.id
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/tickets/project/{project_id}", response_model=List[AfterSalesTicketRead], summary="按项目获取工单", description="查询特定项目相关的所有售后记录。")
def list_project_tickets(
    project_id: int = Path(..., description="项目ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目关联的售后工单"""
    return after_sales_ticket_crud.get_by_project(db, project_id)


# ============================================================
# 改稿日志
# ============================================================

@router.post("/revisions", response_model=RevisionLogRead, summary="添加改稿记录", description="手动录入一次改稿行为，系统会自动增加任务的改稿计数。")
def add_revision_record(
    task_id: int = Query(..., description="任务ID"),
    description: str = Query(..., description="改稿需求描述"),
    is_paid: str = Query("false", description="是否付费"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """添加改稿记录"""
    revision = revision_log_crud.add_revision(
        db, task_id, description, 
        designer_id=current_user.id, 
        is_paid=is_paid
    )
    if not revision:
        raise HTTPException(status_code=404, detail="任务不存在")
    return revision


@router.get("/revisions/task/{task_id}", response_model=List[RevisionLogRead], summary="获取改稿历史", description="查询单个任务的所有历史改稿细节。")
def list_task_revisions(
    task_id: int = Path(..., description="任务ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务改稿历史"""
    return revision_log_crud.get_by_task(db, task_id)
