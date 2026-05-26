from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from database.db import get_db
from models.user import User
from models.approval import Approval
from config.auth import get_current_user
from schemas.approval_schema import ApprovalRead, ApprovalCreate
from datetime import datetime

router = APIRouter()

# ============================================================
# 审批流 (Approvals)
# ============================================================

@router.post("", response_model=ApprovalRead, summary="提交审批")
def create_approval(
    a_in: ApprovalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_obj = Approval(**a_in.model_dump(), requester_id=current_user.id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.put("/{id}/pass", summary="审批通过")
def pass_approval(
    id: int = Path(..., description="审批记录ID"),
    reason: Optional[str] = Body(None, embed=True, description="审批意见"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    a = db.query(Approval).filter(Approval.id == id).first()
    if not a:
        raise HTTPException(status_code=404, detail="审批记录不存在")
    
    a.status = "approved"
    a.reason = reason
    a.finish_time = datetime.utcnow()
    db.commit()
    return {"message": "审批已通过"}


@router.put("/{id}/reject", summary="审批驳回")
def reject_approval(
    id: int = Path(..., description="审批记录ID"),
    reason: str = Body(..., embed=True, description="驳回原因"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    a = db.query(Approval).filter(Approval.id == id).first()
    if not a:
        raise HTTPException(status_code=404, detail="审批记录不存在")
    
    a.status = "rejected"
    a.reason = reason
    a.finish_time = datetime.utcnow()
    db.commit()
    return {"message": "审批已驳回"}
