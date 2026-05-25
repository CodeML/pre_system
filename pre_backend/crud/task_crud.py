from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime
from crud.base_crud import BaseCRUD
from models.task import Task
from utils.ecommerce_utils import validate_ecommerce_params


class TaskCRUD(BaseCRUD):
    """任务 CRUD 操作"""

    def create_task(self, db: Session, project_id: int, category_id: int,
                   name: str, designer_id: int = None, role_ids: list = None,
                   progress: float = 0, status: str = "待开始",
                   ecommerce_params: dict = None, deadline: datetime = None,
                   priority: str = "中", description: str = None,
                   remark: str = None, **kwargs):
        """创建任务"""

        # 校验电商参数
        if ecommerce_params:
            platform = ecommerce_params.get("platform")
            validation = validate_ecommerce_params(platform, ecommerce_params)
            if not validation["valid"]:
                raise ValueError(f"电商参数校验失败: {', '.join(validation['errors'])}")

        task = Task(
            project_id=project_id,
            category_id=category_id,
            name=name,
            designer_id=designer_id,
            role_ids=role_ids,
            progress=progress,
            status=status,
            ecommerce_params=ecommerce_params,
            deadline=deadline,
            priority=priority,
            description=description,
            remark=remark,
            **kwargs
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def get_by_project(self, db: Session, project_id: int,
                      skip: int = 0, limit: int = 100) -> List[Task]:
        """按项目查询任务"""
        return db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_by_category(self, db: Session, category_id: int,
                       skip: int = 0, limit: int = 100) -> List[Task]:
        """按分类查询任务"""
        return db.query(self.model).filter(
            self.model.category_id == category_id,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_by_status(self, db: Session, status: str,
                     skip: int = 0, limit: int = 100) -> List[Task]:
        """按状态查询任务"""
        return db.query(self.model).filter(
            self.model.status == status,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_by_designer(self, db: Session, designer_id: int,
                       skip: int = 0, limit: int = 100) -> List[Task]:
        """按设计师查询任务"""
        return db.query(self.model).filter(
            self.model.designer_id == designer_id,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_by_priority(self, db: Session, priority: str,
                       skip: int = 0, limit: int = 100) -> List[Task]:
        """按优先级查询任务"""
        return db.query(self.model).filter(
            self.model.priority == priority,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_by_role(self, db: Session, role_id: int,
                   skip: int = 0, limit: int = 100) -> List[Task]:
        """
        按角色查询任务（role_ids 包含该角色）
        """
        # 使用 filter 查询所有任务，然后在 Python 中过滤
        all_tasks = db.query(self.model).filter(
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

        # 过滤包含该角色 ID 的任务
        filtered_tasks = [
            task for task in all_tasks
            if task.role_ids and role_id in task.role_ids
        ]
        return filtered_tasks

    def filter_by_criteria(self, db: Session, project_id: int = None,
                          category_id: int = None, status: str = None,
                          priority: str = None, designer_id: int = None,
                          role_id: int = None,
                          skip: int = 0, limit: int = 100) -> List[Task]:
        """多条件筛选任务"""
        query = db.query(self.model).filter(self.model.is_active == True)

        if project_id:
            query = query.filter(self.model.project_id == project_id)

        if category_id:
            query = query.filter(self.model.category_id == category_id)

        if status:
            query = query.filter(self.model.status == status)

        if priority:
            query = query.filter(self.model.priority == priority)

        if designer_id:
            query = query.filter(self.model.designer_id == designer_id)

        tasks = query.offset(skip).limit(limit).all()

        # 如果需要按角色过滤
        if role_id:
            tasks = [
                task for task in tasks
                if task.role_ids and role_id in task.role_ids
            ]

        return tasks

    def update_progress(self, db: Session, task_id: int, progress: float) -> Optional[Task]:
        """更新任务进度"""
        if progress < 0 or progress > 100:
            raise ValueError("进度必须在 0-100 之间")

        task = self.get(db, task_id)
        if task:
            old_status = task.status
            task.progress = progress
            # 根据进度自动更新状态
            if progress == 0:
                task.status = "待开始"
            elif progress < 100:
                task.status = "进行中"
            elif progress == 100:
                task.status = "已完成"
                task.end_time = datetime.utcnow()

            db.commit()
            db.refresh(task)
            
            # 触发通知
            if old_status != task.status:
                self._trigger_status_notification(db, task)
        return task

    def update_status(self, db: Session, task_id: int, new_status: str) -> Optional[Task]:
        """更新任务状态"""
        valid_statuses = ["待开始", "进行中", "待确认", "已完成"]
        if new_status not in valid_statuses:
            raise ValueError(f"无效的状态。有效值: {', '.join(valid_statuses)}")

        task = self.get(db, task_id)
        if task:
            old_status = task.status
            task.status = new_status
            if new_status == "进行中" and not task.start_time:
                task.start_time = datetime.utcnow()
            elif new_status == "已完成":
                task.end_time = datetime.utcnow()
                task.progress = 100

            db.commit()
            db.refresh(task)
            
            # 触发通知
            if old_status != new_status:
                self._trigger_status_notification(db, task)
        return task

    def assign_designer(self, db: Session, task_id: int, designer_id: int) -> Optional[Task]:
        """分配设计师"""
        task = self.get(db, task_id)
        if task:
            task.designer_id = designer_id
            db.commit()
            db.refresh(task)
            
            # 触发任务分配通知
            self._trigger_assignment_notification(db, task, designer_id)
        return task

    def add_role(self, db: Session, task_id: int, role_id: int) -> Optional[Task]:
        """添加角色"""
        task = self.get(db, task_id)
        if task:
            if task.role_ids is None:
                task.role_ids = []
            if role_id not in task.role_ids:
                task.role_ids.append(role_id)
            db.commit()
            db.refresh(task)
        return task

    def remove_role(self, db: Session, task_id: int, role_id: int) -> Optional[Task]:
        """移除角色"""
        task = self.get(db, task_id)
        if task and task.role_ids and role_id in task.role_ids:
            task.role_ids.remove(role_id)
            db.commit()
            db.refresh(task)
        return task

    def update_ecommerce_params(self, db: Session, task_id: int,
                               ecommerce_params: dict) -> Optional[Task]:
        """更新电商参数"""
        # 校验电商参数
        platform = ecommerce_params.get("platform")
        validation = validate_ecommerce_params(platform, ecommerce_params)
        if not validation["valid"]:
            raise ValueError(f"电商参数校验失败: {', '.join(validation['errors'])}")

        task = self.get(db, task_id)
        if task:
            task.ecommerce_params = ecommerce_params
            db.commit()
            db.refresh(task)
        return task

    def get_overdue_tasks(self, db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
        """获取逾期任务"""
        return db.query(self.model).filter(
            self.model.deadline < datetime.utcnow(),
            self.model.status != "已完成",
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_upcoming_tasks(self, db: Session, days: int = 7,
                          skip: int = 0, limit: int = 100) -> List[Task]:
        """获取即将到期的任务（N天内）"""
        from datetime import timedelta
        future_date = datetime.utcnow() + timedelta(days=days)
        return db.query(self.model).filter(
            self.model.deadline <= future_date,
            self.model.deadline >= datetime.utcnow(),
            self.model.status != "已完成",
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_project_progress(self, db: Session, project_id: int) -> dict:
        """获取项目整体进度"""
        tasks = db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.is_active == True
        ).all()

        if not tasks:
            return {
                "total": 0,
                "completed": 0,
                "in_progress": 0,
                "pending": 0,
                "average_progress": 0,
                "completion_rate": "0%"
            }

        total = len(tasks)
        completed = len([t for t in tasks if t.status == "已完成"])
        in_progress = len([t for t in tasks if t.status == "进行中"])
        pending = len([t for t in tasks if t.status == "待开始"])

        avg_progress = sum(t.progress for t in tasks) / total if tasks else 0
        completion_rate = (completed / total * 100) if total > 0 else 0

        return {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "average_progress": round(avg_progress, 2),
            "completion_rate": f"{round(completion_rate, 1)}%"
        }

    def _trigger_status_notification(self, db: Session, task: Task):
        """触发任务状态变更通知"""
        try:
            from utils.notification_utils import NotificationManager
            
            if task.status == "已完成":
                # 任务完成通知
                NotificationManager.notify_task_completed(
                    db, 
                    task=task,
                    completed_by_id=task.designer_id
                )
            elif task.status == "进行中":
                # 任务状态变更通知
                NotificationManager.notify_status_changed(
                    db,
                    task=task,
                    new_status="进行中"
                )
        except Exception as e:
            # 通知失败不应影响主业务逻辑
            print(f"通知触发失败: {e}")

    def _trigger_assignment_notification(self, db: Session, task: Task, designer_id: int):
        """触发任务分配通知"""
        try:
            from utils.notification_utils import NotificationManager
            
            NotificationManager.notify_task_assigned(
                db,
                task=task,
                assigned_to_id=designer_id
            )
        except Exception as e:
            # 通知失败不应影响主业务逻辑
            print(f"通知触发失败: {e}")

    def batch_update_status(self, db: Session, task_ids: List[int], status: str) -> dict:
        """批量更新任务状态"""
        updated = 0
        for task_id in task_ids:
            task = self.get(db, task_id)
            if task:
                self.update(db, task_id, {"status": status})
                updated += 1
        return {"updated": updated, "total": len(task_ids)}

    def batch_update_priority(self, db: Session, task_ids: List[int], priority: str) -> dict:
        """批量更新任务优先级"""
        updated = 0
        for task_id in task_ids:
            task = self.get(db, task_id)
            if task:
                self.update(db, task_id, {"priority": priority})
                updated += 1
        return {"updated": updated, "total": len(task_ids)}

    def batch_assign_designer(self, db: Session, task_ids: List[int], designer_id: int) -> dict:
        """批量分配设计师"""
        updated = 0
        for task_id in task_ids:
            task = self.get(db, task_id)
            if task:
                self.update(db, task_id, {"designer_id": designer_id})
                updated += 1
        return {"updated": updated, "total": len(task_ids)}

    def batch_delete(self, db: Session, task_ids: List[int]) -> dict:
        """批量删除任务"""
        deleted = 0
        for task_id in task_ids:
            task = self.get(db, task_id)
            if task:
                self.update(db, task_id, {"is_active": False})
                deleted += 1
        return {"deleted": deleted, "total": len(task_ids)}

    def export_to_dict(self, db: Session, task_ids: List[int] = None, 
                      project_id: int = None) -> List[dict]:
        """导出任务为字典列表"""
        if task_ids:
            tasks = [self.get(db, tid) for tid in task_ids]
            tasks = [t for t in tasks if t]
        elif project_id:
            tasks = self.get_by_project(db, project_id, skip=0, limit=10000)
        else:
            tasks = self.get_list(db, skip=0, limit=10000)
        
        result = []
        for task in tasks:
            result.append({
                "id": task.id,
                "name": task.name,
                "project_id": task.project_id,
                "category_id": task.category_id,
                "designer_id": task.designer_id,
                "status": task.status,
                "priority": task.priority,
                "progress": task.progress,
                "deadline": task.deadline.isoformat() if task.deadline else None,
                "description": task.description,
                "create_time": task.create_time.isoformat() if task.create_time else None
            })
        return result


# 创建全局实例
task_crud = TaskCRUD(Task)

