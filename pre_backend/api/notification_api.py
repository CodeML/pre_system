"""
通知 API
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Response, Path
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from config.auth import get_current_user
from database.db import get_db
from models.user import User
from crud.notification_crud import notification_crud
from schemas.notification_schema import (
    NotificationRead, NotificationCreate, NotificationStatistics, NotificationUpdate
)

router = APIRouter()


@router.get("/list", response_model=List[NotificationRead], summary="获取通知列表", description="分页查询当前登录用户接收到的所有通知信息。")
def get_notifications(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(50, ge=1, le=100, description="返回记录数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的通知列表"""
    notifications = notification_crud.get_user_notifications(
        db, current_user.id, skip=skip, limit=limit
    )
    return notifications


@router.get("/unread", response_model=List[NotificationRead], summary="获取未读通知", description="专门筛选当前用户尚未阅读的所有通知。")
def get_unread_notifications(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(50, ge=1, le=100, description="返回记录数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取未读通知"""
    notifications = notification_crud.get_unread_notifications(
        db, current_user.id, skip=skip, limit=limit
    )
    return notifications


@router.get("/unread-count", summary="获取未读总数", description="快速获取当前用户未读通知的数量。")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取未读通知数"""
    count = notification_crud.get_unread_count(db, current_user.id)
    return {"unread_count": count}


@router.put("/{notification_id}", response_model=NotificationRead, summary="更新通知属性", description="修改通知的已读状态或重要程度。")
def update_notification(
    notification_id: int = Path(..., description="通知ID"),
    notification_in: NotificationUpdate = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新通知状态或优先级"""
    notification = notification_crud.get(db, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="通知不存在")
    if notification.recipient_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此通知")

    updated_notification = notification_crud.update(db, notification_id, notification_in)
    return updated_notification


@router.put("/{notification_id}/read", response_model=NotificationRead, summary="标记为已读", description="将单条通知状态快速设置为已读。")
def mark_notification_as_read(
    notification_id: int = Path(..., description="通知ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """标记通知为已读"""
    notification = notification_crud.get(db, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="通知不存在")
    if notification.recipient_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此通知")

    return notification_crud.mark_as_read(db, notification_id)


@router.post("/read-all", summary="全部标记已读", description="一键将当前用户的所有未读通知设为已读。")
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """标记所有通知为已读"""
    count = notification_crud.mark_all_as_read(db, current_user.id)
    return {"marked_as_read": count}


@router.get("/filter/by-type/{notification_type}", response_model=List[NotificationRead], summary="按类型查询", description="按业务类型（如：系统、任务提醒）筛选通知。")
def get_notifications_by_type(
    notification_type: str = Path(..., description="通知类型"),
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(50, ge=1, le=100, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按类型查询通知"""
    notifications = notification_crud.get_by_type(
        db, current_user.id, notification_type, skip=skip, limit=limit
    )
    return notifications


@router.get("/filter/by-priority/{priority}", response_model=List[NotificationRead], summary="按优先级查询", description="按紧急程度（高/中/低）筛选通知。")
def get_notifications_by_priority(
    priority: str = Path(..., description="优先级"),
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(50, ge=1, le=100, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按优先级查询通知"""
    notifications = notification_crud.get_by_priority(
        db, current_user.id, priority, skip=skip, limit=limit
    )
    return notifications


@router.get("/statistics", summary="获取通知统计", description="统计各类通知的数量分布。")
def get_notification_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取通知统计"""
    stats = notification_crud.get_statistics(db, current_user.id)
    return stats


@router.delete("/{notification_id}", summary="删除通知", description="软删除指定的通知记录。")
def delete_notification(
    notification_id: int = Path(..., description="通知ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除通知（软删除）"""
    notification = notification_crud.get(db, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="通知不存在")
    if notification.recipient_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此通知")

    notification_crud.update(db, notification_id, {"is_active": False})
    return {"message": "通知已删除"}


@router.post("/cleanup", summary="清理旧通知", description="批量删除超过指定天数的旧通知，保持系统整洁。")
def cleanup_old_notifications(
    days: int = Query(30, ge=1, le=365, description="保留天数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """清理旧通知"""
    count = notification_crud.delete_old_notifications(db, current_user.id, days=days)
    return {"deleted_count": count, "days": days}


# ============================================================
# 高级统计接口
# ============================================================

@router.get("/statistics/by-date-range", summary="按日期统计", description="按日聚合统计特定时间段内的通知量。")
def get_statistics_by_date_range(
    start_date: Optional[str] = Query(None, description="开始日期 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="结束日期 (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按日期范围获取统计（时间序列聚合）"""
    start = None
    end = None
    try:
        if start_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD")
    
    stats = notification_crud.get_statistics_by_date_range(db, current_user.id, start, end)
    return stats


@router.get("/statistics/by-source", summary="按来源统计", description="统计不同来源（项目、任务、全局）的通知占比。")
def get_statistics_by_source(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按来源分组统计（任务/系统通知）"""
    stats = notification_crud.get_statistics_by_source(db, current_user.id)
    return stats


@router.get("/export/csv", summary="导出为 CSV", description="将用户的通知历史导出为 Excel 可读的 CSV 文件。")
def export_notifications_csv(
    include_content: bool = Query(False, description="是否包含完整内容"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """导出通知为 CSV 文件"""
    csv_content = notification_crud.export_to_csv(db, current_user.id, include_content)
    
    return Response(
        content=csv_content.encode('utf-8-sig'),  # UTF-8 with BOM for Excel
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=notifications.csv"}
    )
