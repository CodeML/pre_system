"""
消息通知工具
- 创建各类通知
- 发送通知
- 标记已读
"""
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from models.notification import Notification
from models.user import User
from models.task import Task
from models.project import Project


class NotificationManager:
    """通知管理器"""

    @staticmethod
    def create_notification(
        db: Session,
        recipient_id: int,
        type: str,
        title: str,
        content: str,
        task_id: Optional[int] = None,
        project_id: Optional[int] = None,
        priority: str = "normal",
        sender_id: Optional[int] = None,
        action_url: Optional[str] = None
    ) -> Notification:
        """创建通知"""
        notification = Notification(
            sender_id=sender_id,
            recipient_id=recipient_id,
            task_id=task_id,
            project_id=project_id,
            type=type,
            title=title,
            content=content,
            priority=priority,
            action_url=action_url
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def notify_task_assigned(
        db: Session,
        task_id: int,
        assignee_id: int,
        assigner_id: int
    ) -> Notification:
        """
        任务分配通知
        """
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError(f"任务 {task_id} 不存在")

        title = f"新任务分配: {task.title}"
        content = f"您被分配了任务: {task.title}，请及时处理"

        return NotificationManager.create_notification(
            db=db,
            recipient_id=assignee_id,
            type="task_assigned",
            title=title,
            content=content,
            task_id=task_id,
            project_id=task.project_id,
            priority="high",
            sender_id=assigner_id,
            action_url=f"/task/{task_id}"
        )

    @staticmethod
    def notify_task_completed(
        db: Session,
        task_id: int,
        completer_id: int,
        watchers: List[int]
    ) -> List[Notification]:
        """
        任务完成通知（发送给关注者）
        """
        notifications = []
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError(f"任务 {task_id} 不存在")

        for watcher_id in watchers:
            if watcher_id != completer_id:  # 不给完成者发送
                title = f"任务已完成: {task.title}"
                content = f"任务 {task.title} 已完成，请检查"

                notification = NotificationManager.create_notification(
                    db=db,
                    recipient_id=watcher_id,
                    type="task_completed",
                    title=title,
                    content=content,
                    task_id=task_id,
                    project_id=task.project_id,
                    priority="normal",
                    sender_id=completer_id,
                    action_url=f"/task/{task_id}"
                )
                notifications.append(notification)

        return notifications

    @staticmethod
    def notify_overdue_task(
        db: Session,
        task_id: int
    ) -> Notification:
        """
        任务超期提醒
        """
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError(f"任务 {task_id} 不存在")

        # 获取负责人
        if not task.designer_id:
            return None

        days_overdue = (datetime.utcnow() - task.deadline).days if task.deadline else 0
        title = f"⚠️ 任务超期: {task.title}"
        content = f"任务 {task.title} 已超期 {days_overdue} 天，请尽快完成"

        return NotificationManager.create_notification(
            db=db,
            recipient_id=task.designer_id,
            type="overdue",
            title=title,
            content=content,
            task_id=task_id,
            project_id=task.project_id,
            priority="urgent",
            action_url=f"/task/{task_id}"
        )

    @staticmethod
    def notify_customer_confirmed(
        db: Session,
        project_id: int,
        customer_id: int,
        project_manager_ids: List[int]
    ) -> List[Notification]:
        """
        客户确认通知（发送给项目经理）
        """
        notifications = []
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError(f"项目 {project_id} 不存在")

        for pm_id in project_manager_ids:
            title = f"客户已确认: {project.title}"
            content = f"项目 {project.title} 已获得客户确认，可继续进行"

            notification = NotificationManager.create_notification(
                db=db,
                recipient_id=pm_id,
                type="customer_confirmed",
                title=title,
                content=content,
                project_id=project_id,
                priority="high",
                sender_id=customer_id,
                action_url=f"/project/{project_id}"
            )
            notifications.append(notification)

        return notifications

    @staticmethod
    def notify_status_changed(
        db: Session,
        task_id: int,
        old_status: str,
        new_status: str,
        notifier_id: int,
        watchers: List[int]
    ) -> List[Notification]:
        """
        任务状态变更通知
        """
        notifications = []
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError(f"任务 {task_id} 不存在")

        for watcher_id in watchers:
            if watcher_id != notifier_id:
                title = f"任务状态更新: {task.title}"
                content = f"任务 {task.title} 的状态已从 {old_status} 更改为 {new_status}"

                notification = NotificationManager.create_notification(
                    db=db,
                    recipient_id=watcher_id,
                    type="status_changed",
                    title=title,
                    content=content,
                    task_id=task_id,
                    project_id=task.project_id,
                    priority="normal",
                    sender_id=notifier_id,
                    action_url=f"/task/{task_id}"
                )
                notifications.append(notification)

        return notifications


# 导出通知管理器
notification_manager = NotificationManager()
