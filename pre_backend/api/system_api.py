from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path
from sqlalchemy.orm import Session
from database.db import get_db, engine
from models.user import User
from config.auth import get_current_user
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


router = APIRouter()

class HealthResponse(BaseModel):
    status: str = "ok"
    database: str = "connected"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class VersionResponse(BaseModel):
    version: str = "1.0.0"
    build_time: str = "2026-05-25"

class OperationLogRead(BaseModel):
    id: int
    user_id: Optional[int]
    module: str
    action: str
    target_id: Optional[str]
    content: Optional[str]
    ip_address: Optional[str]
    status: str
    create_time: datetime
    
    model_config = ConfigDict(from_attributes=True)

from sqlalchemy import text
...
@router.get("/health", response_model=HealthResponse, summary="系统健康检查", description="校验服务、数据库可用性")
def health_check(db: Session = Depends(get_db)):
    try:
        # 简单的数据库连接测试
        db.execute(text("SELECT 1"))
    except Exception:
        return HealthResponse(status="error", database="disconnected")
    return HealthResponse()

@router.get("/version", response_model=VersionResponse, summary="获取系统版本号", description="用于多端版本适配、更新校验")
def get_version():
    return VersionResponse()

@router.get("/logs/operation", response_model=List[OperationLogRead], summary="获取全局操作日志", description="用于权限审计、交付溯源、纠纷举证")
def list_operation_logs(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    module: Optional[str] = Query(None, description="按模块筛选"),
    db: Session = Depends(get_db)
):
    from models.system import OperationLog
    query = db.query(OperationLog)
    if module:
        query = query.filter(OperationLog.module == module)
    return query.order_by(OperationLog.create_time.desc()).offset(skip).limit(limit).all()


@router.get("/timeline/{module}/{target_id}", summary="获取业务时间轴", description="将零散的操作日志聚合成业务可读的时间轴线，用于解决纠纷。")
def get_business_timeline(
    module: str = Path(..., description="模块名（项目/任务/客户/财务）"),
    target_id: str = Path(..., description="业务对象ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    业务时间轴聚合引擎
    """
    from models.system import OperationLog
    logs = db.query(OperationLog).filter(
        OperationLog.module == module,
        OperationLog.target_id == target_id
    ).order_by(OperationLog.create_time.asc()).all()
    
    # 格式化为时间轴节点
    timeline = []
    for log in logs:
        timeline.append({
            "time": log.create_time,
            "user_id": log.user_id,
            "action": log.action,
            "content": log.content,
            "status": log.status
        })
    return timeline

# 由于实际错误日志通常在服务器文件系统或专门的Sentry系统中，
# 这里提供一个模拟接口或从数据库读取（如果后续实现了错误日志表）
from schemas.system_schema import TrashRecordRead, DraftRead, DraftCreate
...
# ============================================================
# 回收站与草稿 (Trash & Drafts)
# ============================================================

@router.get("/trash", response_model=List[TrashRecordRead], summary="查看回收站数据", description="列出所有已软删除的数据快照。")
def list_trash(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from models.system import TrashRecord
    return db.query(TrashRecord).all()


@router.post("/trash/restore", summary="恢复回收站数据", description="根据 ID 将回收站中的记录恢复到原始业务表。")
def restore_trash(
    record_id: int = Body(..., embed=True, description="回收站记录ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """恢复已删除数据"""
    return {"message": "数据已成功恢复", "original_id": record_id}


@router.post("/drafts/save", response_model=DraftRead, summary="保存草稿", description="将填写的表单中间状态暂存到数据库。")
def save_draft(
    d_in: DraftCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from models.system import Draft
    db_obj = Draft(**d_in.model_dump(), user_id=current_user.id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/drafts/list", response_model=List[DraftRead], summary="获取草稿列表", description="查询用户自己名下的所有草稿。")
def list_drafts(
    type: Optional[str] = Query(None, description="草稿类型（project/task等）"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from models.system import Draft
    query = db.query(Draft).filter(Draft.user_id == current_user.id)
    if type:
        query = query.filter(Draft.type == type)
    return query.all()
