from apscheduler.schedulers.background import BackgroundScheduler
from database.db import get_db
from models.task import Task
from models.finance import ProjectBudget
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("pre_system.scheduler")

def check_overdue_tasks():
    """定时检查逾期任务"""
    db = next(get_db())
    try:
        now = datetime.utcnow()
        overdue = db.query(Task).filter(
            Task.deadline < now,
            Task.status != '已完成',
            Task.is_deleted == False
        ).all()
        if overdue:
            logger.info(f"[Scheduler] Found {len(overdue)} overdue tasks.")
            # 逻辑占位：触发通知
    finally:
        db.close()

def check_budget_risk():
    """定时检查预算风险"""
    db = next(get_db())
    try:
        alerts = db.query(ProjectBudget).filter(
            ProjectBudget.actual_cost >= ProjectBudget.budget_amount * ProjectBudget.risk_threshold
        ).all()
        if alerts:
            logger.warning(f"[Scheduler] Found {len(alerts)} projects at budget risk.")
    finally:
        db.close()

def archive_old_logs():
    """定时归档180天前的日志"""
    db = next(get_db())
    try:
        from models.system import OperationLog
        threshold = datetime.utcnow() - timedelta(days=180)
        # 逻辑模拟：实际应移动到 Archive 表
        count = db.query(OperationLog).filter(OperationLog.create_time < threshold).count()
        if count > 0:
            logger.info(f"[Scheduler] {count} old logs ready for archiving.")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # 每小时检查一次逾期
    scheduler.add_job(check_overdue_tasks, 'interval', hours=1)
    # 每天凌晨检查一次预算
    scheduler.add_job(check_budget_risk, 'cron', hour=2)
    # 每周归档一次日志
    scheduler.add_job(archive_old_logs, 'cron', day_of_week='sun', hour=3)
    
    scheduler.start()
    logger.info("⏰ Background Scheduler started.")
