from crud.base_crud import BaseCRUD
from models.hr import AttendanceRecord, Timesheet, PerformanceReview
from sqlalchemy.orm import Session
from datetime import datetime


class AttendanceCRUD(BaseCRUD):
    def check_in(self, db: Session, user_id: int, location: str = None, device_info: str = None, remark: str = None):
        """签到"""
        today = datetime.utcnow().date()
        # 检查今天是否已经有记录
        existing = db.query(self.model).filter(
            self.model.user_id == user_id,
            # 这里简单处理，实际应按日期筛选
        ).order_by(self.model.create_time.desc()).first()
        
        # 简化逻辑：直接创建新记录
        db_obj = self.model(
            user_id=user_id,
            check_in_time=datetime.utcnow(),
            location=location,
            device_info=device_info,
            remark=remark
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def check_out(self, db: Session, user_id: int):
        """签退"""
        # 找到最近的一条没有签退时间的记录
        record = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.check_out_time == None
        ).order_by(self.model.create_time.desc()).first()
        
        if record:
            record.check_out_time = datetime.utcnow()
            db.commit()
            db.refresh(record)
        return record


class TimesheetCRUD(BaseCRUD):
    def get_user_timesheets(self, db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(self.model.user_id == user_id).offset(skip).limit(limit).all()


class PerformanceCRUD(BaseCRUD):
    def get_by_user(self, db: Session, user_id: int):
        return db.query(self.model).filter(self.model.user_id == user_id).all()


attendance_crud = AttendanceCRUD(AttendanceRecord)
timesheet_crud = TimesheetCRUD(Timesheet)
performance_crud = PerformanceCRUD(PerformanceReview)
