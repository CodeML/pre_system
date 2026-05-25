from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL
from models.base import Base

# 导入所有模型以确保它们被 Base 识别
from models.user import User
from models.role import Role
from models.user_role import UserRole
from models.permission import Permission, role_permissions
from models.customer import Customer
from models.customer_tag import CustomerTag, CustomerTagAssociation
from models.task_category import TaskCategory
from models.project import Project
from models.task import Task
from models.task_comment import TaskComment
from models.file import File
from models.material import Material
from models.notification import Notification
from models.finance import FinanceRecord, ProjectBudget, Contract, Invoice
from models.after_sales import AfterSalesTicket, RevisionLog
from models.hr import AttendanceRecord, Timesheet, PerformanceReview
from models.crm import SalesLead, DesignPackage, CaseWork
from models.im import ChatSession, ChatSessionMember, ChatMessage

# 创建引擎
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite专属配置
)
# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 初始化数据库（创建所有表）
def init_db():
    Base.metadata.create_all(bind=engine)

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
