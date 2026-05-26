from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from database.db import get_db
from models.user import User
from config.auth import get_current_user
from pydantic import BaseModel, Field, ConfigDict
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


@router.get("/attendance/me", response_model=List[AttendanceRecordRead], summary="我的考勤", description="查询个人历史打卡明细。")
def get_my_attendance(
    skip: int = Query(0, description="跳过数"),
    limit: int = Query(31, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """查询个人打卡历史"""
    from models.hr import AttendanceRecord
    return db.query(AttendanceRecord).filter(AttendanceRecord.user_id == current_user.id).order_by(AttendanceRecord.create_time.desc()).offset(skip).limit(limit).all()


@router.get("/attendance/user/{user_id}", response_model=List[AttendanceRecordRead], summary="查询员工考勤", description="管理员查看指定员工的考勤数据。")
def get_user_attendance(
    user_id: int = Path(..., description="员工ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """管理员查询员工考勤"""
    from models.hr import AttendanceRecord
    return db.query(AttendanceRecord).filter(AttendanceRecord.user_id == user_id).order_by(AttendanceRecord.create_time.desc()).all()


@router.get("/performance/user/{user_id}", response_model=List[PerformanceReviewRead], summary="查询员工绩效", description="管理员查看指定员工的所有绩效评审记录。")
def get_user_performance(
    user_id: int = Path(..., description="员工ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """管理员查询员工绩效"""
    return performance_crud.get_by_user(db, user_id)


# ============= Performance Review Schemas =============
class PerformanceReviewCreate(BaseModel):
    user_id: int
    period: str
    score: int
    rating: str
    summary: Optional[str] = None
    bonus_amount: int = 0


@router.post("/performance/review", response_model=PerformanceReviewRead, summary="提交绩效评审", description="管理员对员工进行月度/季度绩效打分。")
def create_performance_review(
    review_in: PerformanceReviewCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """提交绩效考核结果"""
    return performance_crud.create(db, review_in)


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
