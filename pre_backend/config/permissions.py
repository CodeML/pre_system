"""
RBAC 权限控制模块
提供基于角色的权限装饰器和工具函数
"""

from functools import wraps
from typing import List, Optional, Callable, Any
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.user import User
from config.auth import get_current_user
from config.exceptions import AuthorizationException


# ============= 权限定义 =============

class PermissionEnum:
    """权限枚举"""
    # 用户权限
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    
    # 角色权限
    ROLE_CREATE = "role:create"
    ROLE_READ = "role:read"
    ROLE_UPDATE = "role:update"
    ROLE_DELETE = "role:delete"
    
    # 客户权限
    CUSTOMER_CREATE = "customer:create"
    CUSTOMER_READ = "customer:read"
    CUSTOMER_UPDATE = "customer:update"
    CUSTOMER_DELETE = "customer:delete"
    
    # 项目权限
    PROJECT_CREATE = "project:create"
    PROJECT_READ = "project:read"
    PROJECT_UPDATE = "project:update"
    PROJECT_DELETE = "project:delete"
    
    # 任务权限
    TASK_CREATE = "task:create"
    TASK_READ = "task:read"
    TASK_UPDATE = "task:update"
    TASK_DELETE = "task:delete"
    
    # 文件权限
    FILE_CREATE = "file:create"
    FILE_READ = "file:read"
    FILE_UPDATE = "file:update"
    FILE_DELETE = "file:delete"
    
    # 素材权限
    MATERIAL_CREATE = "material:create"
    MATERIAL_READ = "material:read"
    MATERIAL_UPDATE = "material:update"
    MATERIAL_DELETE = "material:delete"
    
    # 管理权限
    ADMIN = "admin:all"


class RoleEnum:
    """角色枚举"""
    ADMIN = "admin"
    MANAGER = "manager"
    DESIGNER = "designer"
    MODELER = "modeler"
    PHOTOGRAPHER = "photographer"
    CUSTOMER = "customer"


# ============= 角色权限映射 =============

ROLE_PERMISSIONS = {
    RoleEnum.ADMIN: ["*"],  # 管理员拥有所有权限
    
    RoleEnum.MANAGER: [
        PermissionEnum.USER_READ,
        PermissionEnum.ROLE_READ,
        PermissionEnum.CUSTOMER_READ,
        PermissionEnum.CUSTOMER_UPDATE,
        PermissionEnum.PROJECT_READ,
        PermissionEnum.PROJECT_UPDATE,
        PermissionEnum.TASK_READ,
        PermissionEnum.TASK_UPDATE,
        PermissionEnum.FILE_READ,
        PermissionEnum.MATERIAL_READ,
    ],
    
    RoleEnum.DESIGNER: [
        PermissionEnum.CUSTOMER_READ,
        PermissionEnum.PROJECT_READ,
        PermissionEnum.TASK_READ,
        PermissionEnum.TASK_UPDATE,  # 可更新任务进度
        PermissionEnum.FILE_CREATE,
        PermissionEnum.FILE_READ,
        PermissionEnum.FILE_UPDATE,
        PermissionEnum.MATERIAL_READ,
    ],
    
    RoleEnum.MODELER: [
        PermissionEnum.PROJECT_READ,
        PermissionEnum.TASK_READ,
        PermissionEnum.TASK_UPDATE,
        PermissionEnum.FILE_CREATE,
        PermissionEnum.FILE_READ,
        PermissionEnum.FILE_UPDATE,
        PermissionEnum.MATERIAL_READ,
    ],
    
    RoleEnum.PHOTOGRAPHER: [
        PermissionEnum.PROJECT_READ,
        PermissionEnum.TASK_READ,
        PermissionEnum.TASK_UPDATE,
        PermissionEnum.FILE_CREATE,
        PermissionEnum.FILE_READ,
        PermissionEnum.FILE_UPDATE,
        PermissionEnum.MATERIAL_READ,
    ],
    
    RoleEnum.CUSTOMER: [
        PermissionEnum.PROJECT_READ,
        PermissionEnum.TASK_READ,
        PermissionEnum.FILE_READ,
    ],
}


# ============= 权限校验函数 =============

def get_user_roles(db: Session, user_id: int) -> List[str]:
    """获取用户的所有角色编码"""
    from crud.user_role_crud import user_role_crud
    user_roles = user_role_crud.get_user_roles(db, user_id)
    return [role.code for role in user_roles]


def get_user_permissions(db: Session, user_id: int) -> set:
    """获取用户的所有权限"""
    # 尝试基于数据库中的 Role->Permission 结构化关系获取权限
    try:
        role_objs = get_user_roles(db, user_id)
        perms = set()
        for role in role_objs:
            # 如果 role 对象有 permissions 关系，从中读取 code
            if hasattr(role, "permissions") and role.permissions:
                for p in role.permissions:
                    perms.add(p.code)
            else:
                # 回退到在内存映射中查找
                role_perms = ROLE_PERMISSIONS.get(role.code if hasattr(role, 'code') else role, [])
                if "*" in role_perms:
                    return {"*"}
                perms.update(role_perms)

        # 如果集合中包含 '*' 则返回通配
        if "*" in perms:
            return {"*"}
        return perms
    except Exception:
        # 任何问题时，回退到原有静态映射逻辑
        user_roles = get_user_roles(db, user_id)
        permissions = set()
        for role_code in user_roles:
            role_perms = ROLE_PERMISSIONS.get(role_code, [])
            if "*" in role_perms:
                return {"*"}
            permissions.update(role_perms)
        return permissions


def has_permission(db: Session, user_id: int, permission: str) -> bool:
    """检查用户是否拥有指定权限"""
    user_perms = get_user_permissions(db, user_id)
    
    # 如果用户拥有 "*"，则拥有所有权限
    if "*" in user_perms:
        return True
    
    return permission in user_perms


def has_any_role(db: Session, user_id: int, roles: List[str]) -> bool:
    """检查用户是否拥有指定角色中的任何一个"""
    user_roles = get_user_roles(db, user_id)
    return any(role in user_roles for role in roles)


def has_all_roles(db: Session, user_id: int, roles: List[str]) -> bool:
    """检查用户是否拥有所有指定角色"""
    user_roles = get_user_roles(db, user_id)
    return all(role in user_roles for role in roles)


# ============= 权限装饰器 =============

def require_roles(*allowed_roles: str):
    """
    装饰器：检查用户是否拥有指定角色
    
    用法:
        @router.get("/admin-only")
        @require_roles("admin", "manager")
        def admin_endpoint(current_user: User = Depends(get_current_user)):
            return {"message": "只有 admin 或 manager 可访问"}
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # 从 kwargs 中获取当前用户和数据库会话
            current_user: User = kwargs.get("current_user")
            db: Session = kwargs.get("db")
            
            if not current_user or not db:
                raise AuthorizationException("缺少必要的认证信息")
            
            user_roles = get_user_roles(db, current_user.id)
            
            if not any(role in user_roles for role in allowed_roles):
                raise AuthorizationException(
                    f"需要以下角色之一: {', '.join(allowed_roles)}"
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator


def require_permissions(*required_permissions: str):
    """
    装饰器：检查用户是否拥有指定权限
    
    用法:
        @router.post("/project")
        @require_permissions("project:create")
        def create_project(current_user: User = Depends(get_current_user)):
            return {"message": "只有拥有 project:create 权限的用户可访问"}
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            current_user: User = kwargs.get("current_user")
            db: Session = kwargs.get("db")
            
            if not current_user or not db:
                raise AuthorizationException("缺少必要的认证信息")
            
            user_perms = get_user_permissions(db, current_user.id)
            
            # 如果用户拥有 "*"，则拥有所有权限
            if "*" not in user_perms:
                missing_perms = set(required_permissions) - user_perms
                if missing_perms:
                    raise AuthorizationException(
                        f"缺少权限: {', '.join(missing_perms)}"
                    )
            
            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator


def require_any_role(*allowed_roles: str):
    """
    装饰器：检查用户是否拥有指定角色中的任何一个
    别名: require_roles
    """
    return require_roles(*allowed_roles)


def require_admin():
    """装饰器：检查用户是否为管理员"""
    return require_roles(RoleEnum.ADMIN)


# ============= 权限校验依赖 =============

def check_role_dependency(*allowed_roles: str):
    """
    依赖注入工厂：返回一个依赖函数来检查角色
    
    用法:
        @router.get("/protected")
        def protected_route(
            current_user: User = Depends(get_current_user),
            _ = Depends(check_role_dependency("admin", "manager"))
        ):
            return {"user": current_user}
    """
    async def check_role(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        if not has_any_role(db, current_user.id, list(allowed_roles)):
            raise AuthorizationException(
                f"需要以下角色之一: {', '.join(allowed_roles)}"
            )
        return current_user
    
    return check_role


def check_permission_dependency(*required_permissions: str):
    """
    依赖注入工厂：返回一个依赖函数来检查权限
    
    用法:
        @router.post("/project")
        def create_project(
            current_user: User = Depends(get_current_user),
            _ = Depends(check_permission_dependency("project:create"))
        ):
            return {"message": "项目创建成功"}
    """
    async def check_permission(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        for perm in required_permissions:
            if not has_permission(db, current_user.id, perm):
                raise AuthorizationException(f"缺少权限: {perm}")
        return current_user
    
    return check_permission


# ============= 权限信息获取 =============

def get_role_info(role_code: str) -> dict:
    """获取角色信息（包括权限列表）"""
    perms = ROLE_PERMISSIONS.get(role_code, [])
    return {
        "code": role_code,
        "permissions": perms,
        "has_admin": "*" in perms
    }


def get_all_roles_info() -> dict:
    """获取所有角色信息"""
    return {
        role_code: get_role_info(role_code)
        for role_code in ROLE_PERMISSIONS.keys()
    }
