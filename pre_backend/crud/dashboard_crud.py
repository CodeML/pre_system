"""
仪表板 CRUD - 多维度统计聚合
"""
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from models.task import Task
from models.project import Project
from models.user import User
from models.task_category import TaskCategory
from models.user_role import UserRole
from models.role import Role


class DashboardCRUD:
    """仪表板统计操作"""

    # ============= 项目统计 =============

    @staticmethod
    def get_project_stats(db: Session, user_id: int = None) -> dict:
        """
        获取项目统计
        - 总项目数
        - 按状态分类
        - 完成率
        """
        query = db.query(Project).filter(Project.is_active == True)

        if user_id:
            # 仅获取用户参与的项目（设计师或项目经理）
            # 这里简化为返回所有项目，实际应该根据用户角色过滤
            pass

        all_projects = query.all()
        total = len(all_projects)

        # 按状态统计
        status_stats = {}
        for project in all_projects:
            status = project.status or "未知"
            status_stats[status] = status_stats.get(status, 0) + 1

        # 计算完成率
        completed_count = sum(1 for p in all_projects if p.status == "已交付")
        completion_rate = round(completed_count / total * 100, 2) if total > 0 else 0

        return {
            "total_projects": total,
            "status_breakdown": status_stats,
            "completion_rate": completion_rate,
            "completed": completed_count,
            "in_progress": status_stats.get("设计中", 0),
            "pending": status_stats.get("待启动", 0),
            "pending_confirm": status_stats.get("待确认", 0)
        }

    # ============= 任务统计 =============

    @staticmethod
    def get_task_stats(db: Session, user_id: int = None) -> dict:
        """
        获取任务统计
        - 总任务数
        - 按状态分类
        - 按优先级分类
        - 按类别分类
        """
        query = db.query(Task).filter(Task.is_active == True)

        if user_id:
            # 获取分配给用户的任务
            query = query.filter(Task.designer_id == user_id)

        all_tasks = query.all()
        total = len(all_tasks)

        # 按状态统计
        status_stats = {}
        for task in all_tasks:
            status = task.status or "待开始"
            status_stats[status] = status_stats.get(status, 0) + 1

        # 按优先级统计
        priority_stats = {}
        for task in all_tasks:
            priority = task.priority or "普通"
            priority_stats[priority] = priority_stats.get(priority, 0) + 1

        # 按类别统计
        category_stats = {}
        for task in all_tasks:
            if task.category_id:
                category = db.query(TaskCategory).filter(
                    TaskCategory.id == task.category_id
                ).first()
                if category:
                    category_stats[category.name] = category_stats.get(category.name, 0) + 1

        # 进度统计
        avg_progress = round(sum(t.progress or 0 for t in all_tasks) / total, 2) if total > 0 else 0

        return {
            "total_tasks": total,
            "status_breakdown": status_stats,
            "priority_breakdown": priority_stats,
            "category_breakdown": category_stats,
            "average_progress": avg_progress,
            "completed": status_stats.get("已完成", 0),
            "in_progress": status_stats.get("进行中", 0),
            "pending": status_stats.get("待开始", 0)
        }

    # ============= 超期统计 =============

    @staticmethod
    def get_overdue_tasks(db: Session, user_id: int = None) -> dict:
        """
        获取超期任务统计
        """
        query = db.query(Task).filter(
            Task.is_active == True,
            Task.status != "已完成"  # 排除已完成的任务
        )

        if user_id:
            query = query.filter(Task.designer_id == user_id)

        all_tasks = query.all()
        now = datetime.utcnow()

        overdue_tasks = []
        for task in all_tasks:
            if task.deadline and task.deadline < now:
                days_overdue = (now - task.deadline).days
                overdue_tasks.append({
                    "task_id": task.id,
                    "task_name": task.title,
                    "days_overdue": days_overdue,
                    "deadline": task.deadline,
                    "priority": task.priority
                })

        # 按超期天数排序
        overdue_tasks.sort(key=lambda x: x["days_overdue"], reverse=True)

        # 统计超期等级
        overdue_levels = {
            "critical": len([t for t in overdue_tasks if t["days_overdue"] > 7]),
            "high": len([t for t in overdue_tasks if 3 < t["days_overdue"] <= 7]),
            "normal": len([t for t in overdue_tasks if t["days_overdue"] <= 3])
        }

        return {
            "total_overdue": len(overdue_tasks),
            "overdue_levels": overdue_levels,
            "critical_count": overdue_levels["critical"],
            "high_count": overdue_levels["high"],
            "overdue_tasks": overdue_tasks[:10]  # 返回最严重的 10 个
        }

    # ============= 工作量统计 =============

    @staticmethod
    def get_workload_by_designer(db: Session) -> dict:
        """
        按设计师统计工作量
        """
        all_tasks = db.query(Task).filter(Task.is_active == True).all()

        workload = {}
        for task in all_tasks:
            if task.designer_id:
                designer = db.query(User).filter(User.id == task.designer_id).first()
                if designer:
                    if designer.name not in workload:
                        workload[designer.name] = {
                            "user_id": designer.id,
                            "total_tasks": 0,
                            "completed": 0,
                            "in_progress": 0,
                            "pending": 0,
                            "avg_progress": 0,
                            "overdue": 0
                        }

                    workload[designer.name]["total_tasks"] += 1

                    if task.status == "已完成":
                        workload[designer.name]["completed"] += 1
                    elif task.status == "进行中":
                        workload[designer.name]["in_progress"] += 1
                    else:
                        workload[designer.name]["pending"] += 1

                    if task.deadline and task.deadline < datetime.utcnow() and task.status != "已完成":
                        workload[designer.name]["overdue"] += 1

        # 计算平均进度
        for designer in workload.values():
            if designer["total_tasks"] > 0:
                total_progress = sum(
                    t.progress or 0 for t in all_tasks
                    if t.designer_id == designer["user_id"]
                )
                designer["avg_progress"] = round(total_progress / designer["total_tasks"], 2)

        return workload

    # ============= 角色工作量统计 =============

    @staticmethod
    def get_workload_by_role(db: Session) -> dict:
        """
        按角色统计工作量
        """
        all_roles = db.query(Role).filter(Role.is_active == True).all()
        workload = {}

        for role in all_roles:
            # 获取该角色的所有用户
            user_roles = db.query(UserRole).filter(
                UserRole.role_id == role.id
            ).all()
            user_ids = [ur.user_id for ur in user_roles]

            # 获取这些用户的任务
            tasks = db.query(Task).filter(
                Task.is_active == True,
                Task.designer_id.in_(user_ids) if user_ids else False
            ).all()

            completed = len([t for t in tasks if t.status == "已完成"])
            in_progress = len([t for t in tasks if t.status == "进行中"])
            pending = len([t for t in tasks if t.status in ["待开始", "待确认"]])
            overdue = len([t for t in tasks if t.deadline and t.deadline < datetime.utcnow() and t.status != "已完成"])

            workload[role.name] = {
                "role_id": role.id,
                "members": len(user_ids),
                "total_tasks": len(tasks),
                "completed": completed,
                "in_progress": in_progress,
                "pending": pending,
                "overdue": overdue,
                "completion_rate": round(completed / len(tasks) * 100, 2) if tasks else 0
            }

        return workload

    # ============= 平台统计 =============

    @staticmethod
    def get_stats_by_platform(db: Session) -> dict:
        """
        按电商平台统计任务数
        支持: 淘宝, 抖音, 小红书, Amazon 等
        """
        all_tasks = db.query(Task).filter(Task.is_active == True).all()

        platform_stats = {}
        for task in all_tasks:
            if task.ecommerce_params:
                # ecommerce_params 是 JSON 字符串或字典
                params = task.ecommerce_params if isinstance(task.ecommerce_params, dict) else {}
                platform = params.get("platform", "unknown")
            else:
                platform = "未指定"

            if platform not in platform_stats:
                platform_stats[platform] = {
                    "total": 0,
                    "completed": 0,
                    "in_progress": 0,
                    "overdue": 0
                }

            platform_stats[platform]["total"] += 1

            if task.status == "已完成":
                platform_stats[platform]["completed"] += 1
            elif task.status == "进行中":
                platform_stats[platform]["in_progress"] += 1

            if task.deadline and task.deadline < datetime.utcnow() and task.status != "已完成":
                platform_stats[platform]["overdue"] += 1

        return platform_stats

    # ============= 整体仪表板统计 =============

    @staticmethod
    def get_dashboard_overview(db: Session, user_id: int = None) -> dict:
        """
        获取仪表板总体概览
        """
        return {
            "projects": DashboardCRUD.get_project_stats(db, user_id),
            "tasks": DashboardCRUD.get_task_stats(db, user_id),
            "overdue": DashboardCRUD.get_overdue_tasks(db, user_id),
            "timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    def get_full_dashboard(db: Session, user_id: int = None) -> dict:
        """
        获取完整仪表板（包含所有统计）
        """
        return {
            "overview": DashboardCRUD.get_dashboard_overview(db, user_id),
            "workload_by_designer": DashboardCRUD.get_workload_by_designer(db),
            "workload_by_role": DashboardCRUD.get_workload_by_role(db),
            "platform_stats": DashboardCRUD.get_stats_by_platform(db),
            "timestamp": datetime.utcnow().isoformat()
        }


# 创建全局实例
dashboard_crud = DashboardCRUD()
