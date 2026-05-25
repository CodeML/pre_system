from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Time, Float
from models.base import BaseModel
from datetime import datetime


class AttendanceRecord(BaseModel):
    """
    考勤打卡记录
    """
    __tablename__ = "attendance_records"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    check_in_time = Column(DateTime, nullable=True, comment="签到时间")
    check_out_time = Column(DateTime, nullable=True, comment="签退时间")
    
    date = Column(DateTime, default=datetime.utcnow, comment="考勤日期")
    status = Column(String(20), default="normal", comment="状态（normal/late/early_leave/absent）")
    
    location = Column(String(255), nullable=True, comment="打卡地点")
    device_info = Column(String(255), nullable=True, comment="打卡设备信息")
    remark = Column(String(500), nullable=True, comment="备注")


class Timesheet(BaseModel):
    """
    工时填报记录
    """
    __tablename__ = "timesheets"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True, comment="关联任务ID")
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, comment="关联项目ID")
    
    duration = Column(Integer, nullable=False, comment="投入时长（分钟）")
    work_date = Column(DateTime, default=datetime.utcnow, comment="工作日期")
    
    description = Column(String(1000), nullable=False, comment="工作内容描述")
    status = Column(String(20), default="pending", comment="审核状态（pending/approved/rejected）")
    
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="审核人ID")
    reject_reason = Column(String(255), nullable=True, comment="驳回原因")


class PerformanceReview(BaseModel):
    """
    绩效考核台账
    """
    __tablename__ = "performance_reviews"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    period = Column(String(20), nullable=False, comment="考核周期（如：2023-12）")
    
    score = Column(Integer, default=0, comment="绩效评分")
    rating = Column(String(10), comment="绩效等级（A/B/C/D）")
    
    output_count = Column(Integer, default=0, comment="出稿量")
    revision_rate = Column(Float, default=0, comment="平均改稿次数")
    on_time_rate = Column(Float, default=0, comment="准时交付率")
    
    bonus_amount = Column(Integer, default=0, comment="绩效奖金/提成金额")
    summary = Column(String(1000), nullable=True, comment="考核评价汇总")
