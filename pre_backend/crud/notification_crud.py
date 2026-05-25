"""
通知 CRUD 操作
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from crud.base_crud import BaseCRUD
from models.notification import Notification


class NotificationCRUD(BaseCRUD):
    """通知 CRUD 操作"""

    def get_unread_count(self, db: Session, user_id: int) -> int:
        """获取未读通知数"""
        return db.query(self.model).filter(
            self.model.recipient_id == user_id,
            self.model.is_read == False,
            self.model.is_active == True
        ).count()

    def get_unread_notifications(self, db: Session, user_id: int,
                                skip: int = 0, limit: int = 50) -> List[Notification]:
        """获取未读通知列表"""
        return db.query(self.model).filter(
            self.model.recipient_id == user_id,
            self.model.is_read == False,
            self.model.is_active == True
        ).order_by(self.model.create_time.desc()).offset(skip).limit(limit).all()

    def get_user_notifications(self, db: Session, user_id: int,
                              skip: int = 0, limit: int = 50) -> List[Notification]:
        """获取用户所有通知（包括已读）"""
        return db.query(self.model).filter(
            self.model.recipient_id == user_id,
            self.model.is_active == True
        ).order_by(self.model.create_time.desc()).offset(skip).limit(limit).all()

    def mark_as_read(self, db: Session, notification_id: int) -> Optional[Notification]:
        """标记单个通知为已读"""
        notification = self.get(db, notification_id)
        if notification:
            notification.is_read = True
            notification.read_time = datetime.utcnow()
            db.commit()
            db.refresh(notification)
        return notification

    def mark_all_as_read(self, db: Session, user_id: int) -> int:
        """标记用户的所有未读通知为已读"""
        notifications = db.query(self.model).filter(
            self.model.recipient_id == user_id,
            self.model.is_read == False,
            self.model.is_active == True
        ).all()

        for notification in notifications:
            notification.is_read = True
            notification.read_time = datetime.utcnow()

        db.commit()
        return len(notifications)

    def get_by_type(self, db: Session, user_id: int, notification_type: str,
                   skip: int = 0, limit: int = 50) -> List[Notification]:
        """按类型查询用户通知"""
        return db.query(self.model).filter(
            self.model.recipient_id == user_id,
            self.model.type == notification_type,
            self.model.is_active == True
        ).order_by(self.model.create_time.desc()).offset(skip).limit(limit).all()

    def get_by_priority(self, db: Session, user_id: int, priority: str,
                       skip: int = 0, limit: int = 50) -> List[Notification]:
        """按优先级查询用户通知"""
        return db.query(self.model).filter(
            self.model.recipient_id == user_id,
            self.model.priority == priority,
            self.model.is_active == True
        ).order_by(self.model.create_time.desc()).offset(skip).limit(limit).all()

    def get_task_notifications(self, db: Session, task_id: int) -> List[Notification]:
        """获取与某个任务相关的所有通知"""
        return db.query(self.model).filter(
            self.model.task_id == task_id,
            self.model.is_active == True
        ).order_by(self.model.create_time.desc()).all()

    def delete_old_notifications(self, db: Session, user_id: int, days: int = 30) -> int:
        """删除用户 X 天前的通知"""
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        notifications = db.query(self.model).filter(
            self.model.recipient_id == user_id,
            self.model.create_time < cutoff_date,
            self.model.is_active == True
        ).all()

        for notification in notifications:
            notification.is_active = False

        db.commit()
        return len(notifications)

    def get_statistics(self, db: Session, user_id: int) -> dict:
        """获取用户通知统计"""
        all_notifs = db.query(self.model).filter(
            self.model.recipient_id == user_id,
            self.model.is_active == True
        ).all()

        unread = len([n for n in all_notifs if not n.is_read])
        by_type = {}
        by_priority = {}

        for notif in all_notifs:
            by_type[notif.type] = by_type.get(notif.type, 0) + 1
            by_priority[notif.priority] = by_priority.get(notif.priority, 0) + 1

        return {
            "total": len(all_notifs),
            "unread": unread,
            "read": len(all_notifs) - unread,
            "by_type": by_type,
            "by_priority": by_priority
        }

    def get_statistics_by_date_range(self, db: Session, user_id: int, 
                                     start_date: datetime = None, 
                                     end_date: datetime = None) -> dict:
        """按日期范围获取统计（时间序列聚合）"""
        from datetime import timedelta
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()
        
        query = db.query(self.model).filter(
            self.model.recipient_id == user_id,
            self.model.is_active == True,
            self.model.create_time >= start_date,
            self.model.create_time <= end_date
        ).all()
        
        # 按天聚合
        daily_stats = {}
        for notif in query:
            day_key = notif.create_time.strftime("%Y-%m-%d")
            if day_key not in daily_stats:
                daily_stats[day_key] = {"total": 0, "unread": 0, "read": 0}
            daily_stats[day_key]["total"] += 1
            if notif.is_read:
                daily_stats[day_key]["read"] += 1
            else:
                daily_stats[day_key]["unread"] += 1
        
        return {
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "daily_stats": daily_stats,
            "total_in_range": len(query)
        }

    def get_statistics_by_source(self, db: Session, user_id: int) -> dict:
        """按来源分组统计（任务/项目等）"""
        all_notifs = db.query(self.model).filter(
            self.model.recipient_id == user_id,
            self.model.is_active == True
        ).all()
        
        by_source = {}
        for notif in all_notifs:
            source_key = f"task_{notif.task_id}" if notif.task_id else "system"
            if source_key not in by_source:
                by_source[source_key] = {"total": 0, "types": {}, "priorities": {}}
            by_source[source_key]["total"] += 1
            by_source[source_key]["types"][notif.type] = by_source[source_key]["types"].get(notif.type, 0) + 1
            by_source[source_key]["priorities"][notif.priority] = by_source[source_key]["priorities"].get(notif.priority, 0) + 1
        
        return {"by_source": by_source, "source_count": len(by_source)}

    def export_to_csv(self, db: Session, user_id: int, include_content: bool = False) -> str:
        """导出通知为 CSV 格式"""
        import csv
        import io
        
        all_notifs = db.query(self.model).filter(
            self.model.recipient_id == user_id,
            self.model.is_active == True
        ).order_by(self.model.create_time.desc()).all()
        
        output = io.StringIO()
        if include_content:
            fieldnames = ['id', 'type', 'priority', 'title', 'content', 'is_read', 'task_id', 'create_time']
        else:
            fieldnames = ['id', 'type', 'priority', 'title', 'is_read', 'task_id', 'create_time']
        
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for notif in all_notifs:
            row = {
                'id': notif.id,
                'type': notif.type,
                'priority': notif.priority,
                'title': notif.title or '',
                'is_read': 'Yes' if notif.is_read else 'No',
                'task_id': notif.task_id or '',
                'create_time': notif.create_time.isoformat() if notif.create_time else ''
            }
            if include_content:
                row['content'] = notif.content or ''
            writer.writerow(row)
        
        return output.getvalue()


# 创建全局实例
notification_crud = NotificationCRUD(Notification)
