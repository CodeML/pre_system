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
from models.notification import Notification, NotificationSetting, NotificationTemplate
from models.finance import FinanceRecord, ProjectBudget, Contract, Invoice, PaymentOrder, ChangeRequest
from models.after_sales import AfterSalesTicket, RevisionLog
from models.hr import AttendanceRecord, Timesheet, PerformanceReview
from models.crm import SalesLead, DesignPackage, CaseWork
from models.collaboration import Comment
from models.system import OperationLog
from models.extra_features import CustomerFollowUp, ProjectMilestone, TaskReminder
from models.approval import Approval, UnlockRequest
from models.governance import CapabilityTemplate
from models.saas import AsyncJob, Webhook, WebhookLog, EventRecord

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
    
    # 创建默认管理员
    db = SessionLocal()
    try:
        from models.user import User
        from config.auth import get_password_hash
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            # 1. 创建超级管理员
            admin_user = User(
                username="admin",
                password=get_password_hash("123456"),
                name="超级管理员",
                org_id=1,
                is_active=True
            )
            db.add(admin_user)
            db.flush() # 获取ID
            
            # 2. 创建基础角色
            from models.role import Role
            from models.user_role import UserRole
            
            admin_role = Role(name="超级管理员", code="super_admin")
            designer_role = Role(name="设计师", code="executor")
            db.add(admin_role)
            db.add(designer_role)
            db.flush()
            
            # 3. 关联角色
            db.add(UserRole(user_id=admin_user.id, role_id=admin_role.id))
            
            # 4. 创建演示设计师
            designer_user = User(
                username="designer",
                password=get_password_hash("123456"),
                name="首席设计师",
                org_id=1,
                is_active=True
            )
            db.add(designer_user)
            db.flush()
            db.add(UserRole(user_id=designer_user.id, role_id=designer_role.id))
            
            # 5. 创建演示客户
            client_role = Role(name="客户", code="user") # 对应前端 router 的 user
            db.add(client_role)
            db.flush()
            
            client_user = User(
                username="client",
                password=get_password_hash("123456"),
                name="演示客户A",
                org_id=1,
                is_active=True
            )
            db.add(client_user)
            db.flush()
            db.add(UserRole(user_id=client_user.id, role_id=client_role.id))
            
            db.commit()
    finally:
        db.close()

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
