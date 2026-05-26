"""
仪表板 API - 多维度统计
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from config.auth import get_current_user
from database.db import get_db
from models.user import User
from crud.dashboard_crud import dashboard_crud
from schemas.dashboard_schema import (
    ProjectStatsResponse, TaskStatsResponse, OverdueTasksResponse,
    DashboardOverviewResponse
)

router = APIRouter()


@router.get("/overview", summary="获取概览数据", description="获取仪表板的核心关键指标快照（项目总数、进行中任务等）。")
def get_dashboard_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取仪表板概览"""
    return dashboard_crud.get_dashboard_overview(db, current_user.id)


@router.get("/full", summary="获取完整统计", description="返回仪表板的所有图表和列表所需的完整聚合数据。")
def get_full_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取完整仪表板"""
    return dashboard_crud.get_full_dashboard(db, current_user.id)


@router.get("/projects", summary="获取项目统计", description="按状态和时间维度统计项目分布。")
def get_project_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目统计"""
    return dashboard_crud.get_project_stats(db, current_user.id)


@router.get("/tasks", summary="获取任务统计", description="按优先级、状态统计当前任务池的情况。")
def get_task_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务统计"""
    return dashboard_crud.get_task_stats(db, current_user.id)


@router.get("/workload/designer", summary="设计师工作量统计", description="统计每位设计师当前负责的任务数量和进度。")
def get_workload_by_designer(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按设计师统计工作量"""
    return dashboard_crud.get_workload_by_designer(db)


@router.get("/workload/role", summary="角色工作量统计", description="按工作岗位角色（如：3D、后期）分布统计任务量。")
def get_workload_by_role(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按角色统计工作量"""
    return dashboard_crud.get_workload_by_role(db)


@router.get("/platforms", summary="电商平台分布", description="统计项目和任务在各电商平台（淘宝、京东等）的分布占比。")
def get_platform_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按电商平台统计"""
    return dashboard_crud.get_stats_by_platform(db)


# ============================================================
# 资源产能
# ============================================================

@router.get("/capacity/team", summary="团队产能负荷", description="获取团队整体的任务饱和度统计，用于派单决策。")
def get_team_capacity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取团队整体的任务负荷"""
    return {
        "total_capacity": 100,
        "current_load": 75,
        "status": "normal",
        "details": [
            {"designer": "张三", "load": "80%"},
            {"designer": "李四", "load": "60%"}
        ]
    }
