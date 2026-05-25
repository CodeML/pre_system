"""
仪表板 Pydantic 模式
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any


class ProjectStatsResponse(BaseModel):
    """项目统计响应"""
    total_projects: int = Field(..., description="项目总数")
    status_breakdown: Dict[str, int] = Field(..., description="各状态项目分布")
    completion_rate: float = Field(..., description="总体完成率(0-1)")
    completed: int = Field(..., description="已完成数")
    in_progress: int = Field(..., description="设计中数")
    pending: int = Field(..., description="待启动数")
    pending_confirm: int = Field(..., description="待确认数")


class TaskStatsResponse(BaseModel):
    """任务统计响应"""
    total_tasks: int = Field(..., description="任务总数")
    status_breakdown: Dict[str, int] = Field(..., description="各状态任务分布")
    priority_breakdown: Dict[str, int] = Field(..., description="各优先级任务分布")
    category_breakdown: Dict[str, int] = Field(..., description="各分类任务分布")
    average_progress: float = Field(..., description="平均完成进度(0-100)")
    completed: int = Field(..., description="已完成数")
    in_progress: int = Field(..., description="进行中数")
    pending: int = Field(..., description="待开始数")


class OverdueTasksResponse(BaseModel):
    """超期任务响应"""
    total_overdue: int = Field(..., description="超期总数")
    overdue_levels: Dict[str, int] = Field(..., description="超期时长分布")
    critical_count: int = Field(..., description="紧急超期数")
    high_count: int = Field(..., description="高优先级超期数")
    overdue_tasks: List[Dict[str, Any]] = Field(..., description="超期任务简要列表")


class WorkloadResponse(BaseModel):
    """工作量响应"""
    total_tasks: int = Field(..., description="总任务数")
    completed: int = Field(..., description="已完成数")
    in_progress: int = Field(..., description="进行中数")
    pending: int = Field(..., description="待办数")
    overdue: int = Field(..., description="已超期数")
    completion_rate: float = Field(..., description="完成率(0-1)")
    avg_progress: float = Field(..., description="平均进度(0-100)")


class DashboardOverviewResponse(BaseModel):
    """仪表板概览"""
    projects: ProjectStatsResponse = Field(..., description="项目统计概览")
    tasks: TaskStatsResponse = Field(..., description="任务统计概览")
    overdue: OverdueTasksResponse = Field(..., description="超期风险预警")
    timestamp: str = Field(..., description="统计生成时间")


class PlatformStatsResponse(BaseModel):
    """平台统计"""
    platform: str = Field(..., description="平台名称")
    total: int = Field(..., description="总项目/任务数")
    completed: int = Field(..., description="已完成数")
    in_progress: int = Field(..., description="进行中数")
    overdue: int = Field(..., description="已超期数")
