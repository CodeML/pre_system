from sqlalchemy.orm import Session
from models.user import User
from models.role import Role
from models.user_role import UserRole
from typing import List, Dict, Any


def get_user_roles(db: Session, user_id: int) -> List[Dict[str, Any]]:
    """
    聚合用户的所有角色信息
    返回: [{"id": 1, "name": "admin", "code": "ADMIN", ...}, ...]
    """
    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id).all()
    role_ids = [ur.role_id for ur in user_roles]
    
    if not role_ids:
        return []
    
    roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
    return [
        {"id": r.id, "name": r.name, "code": r.code, "permission": r.permission, "is_active": r.is_active}
        for r in roles
    ]


def get_user_role_codes(db: Session, user_id: int) -> List[str]:
    """
    获取用户拥有的所有角色编码列表
    用于权限校验（快速查询）
    """
    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id).all()
    role_ids = [ur.role_id for ur in user_roles]
    
    if not role_ids:
        return []
    
    roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
    return [r.code for r in roles]


def check_user_permission(db: Session, user_id: int, required_role_codes: List[str]) -> bool:
    """
    验证用户是否拥有任一指定的角色（OR逻辑）
    用于接口权限校验装饰器
    """
    user_role_codes = get_user_role_codes(db, user_id)
    return any(code in user_role_codes for code in required_role_codes)
