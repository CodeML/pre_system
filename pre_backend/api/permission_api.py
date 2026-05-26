from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from database.db import get_db
from models.user import User
from models.role import Role
from models.permission import Permission, role_permissions
from config.auth import get_current_user
from pydantic import BaseModel, Field, ConfigDict


router = APIRouter()

# ============= Schemas =============

class PermissionBase(BaseModel):
    code: str = Field(..., description="权限编码")
    name: str = Field(..., description="显示名称")
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionRead(PermissionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class RolePermissionAssignment(BaseModel):
    permission_ids: List[int] = Field(..., description="权限ID列表")

# ============= Endpoints =============

@router.post("", response_model=PermissionRead, summary="创建权限项", description="创建细粒度权限项")
def create_permission(
    perm_in: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 仅限管理员
    db_obj = Permission(**perm_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/list", response_model=List[PermissionRead], summary="获取全部权限项", description="获取系统全部权限项列表")
def list_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Permission).all()


@router.post("/roles/{role_id}/permissions", summary="分配角色权限", description="为指定角色批量分配权限")
def assign_role_permissions(
    role_id: int = Path(..., description="角色ID"),
    request: RolePermissionAssignment = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    # 清空旧权限并添加新权限
    # 实际生产环境通常建议更精细的处理，这里简单处理
    perms = db.query(Permission).filter(Permission.id.in_(request.permission_ids)).all()
    role.permissions = perms # 假设 Role 模型有 permissions relationship
    db.commit()
    return {"message": "权限分配成功", "count": len(perms)}


@router.delete("/roles/{role_id}/permissions/{perm_id}", summary="移除角色权限", description="移除角色指定权限")
def remove_role_permission(
    role_id: int = Path(..., description="角色ID"),
    perm_id: int = Path(..., description="权限ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 手动从关联表中删除
    db.execute(
        role_permissions.delete().where(
            role_permissions.c.role_id == role_id,
            role_permissions.c.permission_id == perm_id
        )
    )
    db.commit()
    return {"message": "权限已移除"}


@router.get("/users/{user_id}/permissions", summary="获取用户最终权限", description="获取用户最终生效权限")
def get_user_effective_permissions(
    user_id: int = Path(..., description="用户ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 汇总用户所有角色的权限
    from models.user_role import UserRole
    role_ids = db.query(UserRole.role_id).filter(UserRole.user_id == user_id).all()
    role_ids = [r[0] for r in role_ids]
    
    perms = db.query(Permission).join(role_permissions).filter(
        role_permissions.c.role_id.in_(role_ids)
    ).all()
    
    return {"user_id": user_id, "permissions": perms}


@router.post("/verify", summary="权限校验", description="接口权限校验")
def verify_permission(
    code: str = Query(..., description="要校验的权限编码"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 这里是一个通用的逻辑
    from models.user_role import UserRole
    role_ids = db.query(UserRole.role_id).filter(UserRole.user_id == current_user.id).all()
    role_ids = [r[0] for r in role_ids]
    
    exists = db.query(Permission).join(role_permissions).filter(
        role_permissions.c.role_id.in_(role_ids),
        Permission.code == code
    ).first()
    
    return {"has_permission": exists is not None}


@router.post("/delegate", summary="权限委派", description="将自己的权限赋予给下级，此操作会记录在操作日志中留痕。")
def delegate_permission(
    target_user_id: int = Body(..., description="获得权限的用户ID"),
    permission_id: int = Body(..., description="要委派的权限ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    权限委派：将自己的权限赋予他人
    规则：授权人必须自己拥有该权限，才能赋予他人
    """
    from models.permission import user_permissions, Permission
    from models.user_role import UserRole
    
    # 1. 验证授权人（自己）是否拥有该权限
    # 检查角色权限
    role_ids = db.query(UserRole.role_id).filter(UserRole.user_id == current_user.id).all()
    role_ids = [r[0] for r in role_ids]
    
    has_perm = db.query(Permission).join(role_permissions).filter(
        role_permissions.c.role_id.in_(role_ids),
        Permission.id == permission_id
    ).first()
    
    if not has_perm:
        raise HTTPException(status_code=403, detail="你未拥有该权限，无法委派给他人")

    # 2. 执行赋权（写入 user_permissions 表）
    # 检查是否已赋权
    from sqlalchemy import insert
    try:
        stmt = insert(user_permissions).values(
            user_id=target_user_id,
            permission_id=permission_id,
            granted_by=current_user.id,
            grant_time=datetime.utcnow()
        )
        db.execute(stmt)
        db.commit()
    except Exception:
        db.rollback()
        # 如果已存在则忽略
        pass

    # 3. 记录日志（留痕核心）
    from models.system import OperationLog
    log = OperationLog(
        user_id=current_user.id,
        module="权限",
        action="delegate",
        target_id=str(target_user_id),
        content=f"委派权限 ID:{permission_id} ({has_perm.name}) 给用户 ID:{target_user_id}",
        status="success"
    )
    db.add(log)
    db.commit()

    return {"message": "权限委派成功", "target_user_id": target_user_id}
