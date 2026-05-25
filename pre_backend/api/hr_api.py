from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from database.db import get_db
from models.user import User
from config.auth import get_current_user
from crud.hr_crud import attendance_crud, timesheet_crud, performance_crud
from schemas.hr_schema import (
    AttendanceRecordRead, AttendanceRecordCreate, 
    TimesheetRead, TimesheetCreate, PerformanceReviewRead
)

router = APIRouter()

# ============================================================
# 考勤打卡
# ============================================================

@router.post("/attendance/check-in", response_model=AttendanceRecordRead, summary="签到", description="记录用户的签到时间和位置信息。")
def check_in(
    record_in: AttendanceRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """签到"""
    return attendance_crud.check_in(
        db, current_user.id, 
        location=record_in.location, 
        device_info=record_in.device_info, 
        remark=record_in.remark
    )


@router.post("/attendance/check-out", response_model=AttendanceRecordRead, summary="签退", description="更新用户当天的签退时间。")
def check_out(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """签退"""
    record = attendance_crud.check_out(db, current_user.id)
    if not record:
        raise HTTPException(status_code=400, detail="未找到对应的签到记录")
    return record


# ============================================================
# 工时填报
# ============================================================

@router.post("/timesheets", response_model=TimesheetRead, summary="填报工时", description="设计师填报在特定任务或项目上投入的时间。")
def create_timesheet(
    timesheet_in: TimesheetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """提交工时"""
    return timesheet_crud.create(db, timesheet_in)


@router.get("/timesheets/me", response_model=List[TimesheetRead], summary="获取我的工时", description="查询当前登录用户的所有工时填报历史。")
def list_my_timesheets(
    skip: int = Query(0, description="跳过数"),
    limit: int = Query(100, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """查询个人工时记录"""
    return timesheet_crud.get_user_timesheets(db, current_user.id, skip, limit)


# ============================================================
# 绩效考核
# ============================================================

@router.get("/performance/me", response_model=List[PerformanceReviewRead], summary="获取我的绩效", description="查看当前用户的月度/季度绩效评估结果。")
def get_my_performance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """查询个人绩效"""
    return performance_crud.get_by_user(db, current_user.id)
