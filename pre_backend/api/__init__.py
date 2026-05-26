from api.user_api import router as user_router
from api.role_api import router as role_router
from api.customer_api import router as customer_router
from api.customer_tag_api import router as customer_tag_router
from api.task_category_api import router as task_category_router
from api.project_api import router as project_router
from api.task_api import router as task_router
from api.file_api import router as file_router
from api.material_api import router as material_router
from api.dashboard_api import router as dashboard_router
from api.notification_api import router as notification_router
from api.notification_template_api import router as notification_template_router
from api.finance_api import router as finance_router
from api.after_sales_api import router as after_sales_router
from api.hr_api import router as hr_router
from api.crm_api import router as crm_router
from api.collaboration_api import router as collaboration_router
from api.system_api import router as system_router
from api.permission_api import router as permission_router
from api.client_api import router as client_router
from api.approval_api import router as approval_router
from api.saas_api import router as saas_router

def register_routers(app):
    app.include_router(system_router, tags=["系统基础"])
    app.include_router(permission_router, prefix="/api/permissions", tags=["权限体系"])
    app.include_router(user_router, prefix="/api/user", tags=["用户管理"])
    app.include_router(role_router, prefix="/api/role", tags=["角色管理"])
    app.include_router(customer_router, prefix="/api/customer", tags=["客户管理"])
    app.include_router(customer_tag_router, prefix="/api/customer-tag", tags=["客户标签"])
    app.include_router(task_category_router, prefix="/api/task-category", tags=["任务分类"])
    app.include_router(project_router, prefix="/api/project", tags=["项目管理"])
    app.include_router(task_router, prefix="/api/task", tags=["任务管理"])
    app.include_router(file_router, prefix="/api/file", tags=["文件管理"])
    app.include_router(material_router, prefix="/api/material", tags=["素材库"])
    app.include_router(dashboard_router, prefix="/api/dashboard", tags=["仪表板"])
    app.include_router(notification_router, prefix="/api/notification", tags=["消息通知"])
    app.include_router(notification_template_router, prefix="/api/notification-templates", tags=["通知模版管理"])
    app.include_router(finance_router, prefix="/api/finance", tags=["财务核算"])
    app.include_router(after_sales_router, prefix="/api/after-sales", tags=["售后风控"])
    app.include_router(hr_router, prefix="/api/hr", tags=["人事绩效"])
    app.include_router(crm_router, prefix="/api/crm", tags=["客户经营"])
    app.include_router(collaboration_router, prefix="/api/collaboration", tags=["协作讨论"])
    app.include_router(client_router, prefix="/api/client-portal", tags=["客户门户"])
    app.include_router(approval_router, prefix="/api/approvals", tags=["审批流管理"])
    app.include_router(saas_router, prefix="/api/saas", tags=["SaaS高级特性"])
