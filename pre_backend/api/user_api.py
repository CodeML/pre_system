from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.db import get_db
from crud.user_crud import user_crud
from crud.user_role_crud import user_role_crud
from models.user import User
from config.auth import verify_password, create_access_token, get_current_user, get_password_hash
from schemas.user_schema import UserCreate, UserRead, TokenWithUser, Token, ChangePasswordRequest, ChangePasswordResponse, UserUpdate
from utils.model_utils import sqlalchemy_to_dict
from utils.auth_utils import get_user_roles
from config.exceptions import raise_auth_error, raise_business_error
from typing import List

# 定义router（与api/__init__.py中引用的变量名一致）
router = APIRouter()

# 示例接口：获取用户列表
@router.get("/list", response_model=List[UserRead], summary="获取用户列表", description="分页获取系统内所有用户的信息")
def get_user_list(
    skip: int = Query(0, description="跳过的记录数"), 
    limit: int = Query(10, description="返回的最大记录数"), 
    db: Session = Depends(get_db)
):
    users = user_crud.get_all(db, skip=skip, limit=limit)
    # exclude sensitive fields
    result = [sqlalchemy_to_dict(u, exclude=["password"]) for u in users]
    return result


@router.put("/{user_id}", response_model=UserRead, summary="更新用户信息", description="更新指定用户的姓名、电话或活跃状态。仅限本人或管理员操作。")
def update_user(
    user_id: int = Path(..., description="要更新的用户ID"),
    user_in: UserUpdate = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新用户信息"""
    user = user_crud.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 只有本人或管理员可以修改用户信息
    from crud.user_role_crud import user_role_crud
    admin_roles = user_role_crud.get_user_roles(db, current_user.id)
    admin_role_names = [role.name for role in admin_roles]
    is_admin = "管理员" in admin_role_names or "超级管理员" in admin_role_names
    
    if current_user.id != user_id and not is_admin:
        raise HTTPException(status_code=403, detail="没有权限修改该用户信息")
    
    updated_user = user_crud.update(db, user, user_in)
    return sqlalchemy_to_dict(updated_user, exclude=["password"])


@router.delete("/{user_id}", summary="禁用用户", description="管理员禁用指定用户（软删除）。")
def delete_user(
    user_id: int = Path(..., description="要禁用的用户ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除或禁用用户"""
    # 验证当前用户是否为管理员
    from crud.user_role_crud import user_role_crud
    admin_roles = user_role_crud.get_user_roles(db, current_user.id)
    admin_role_names = [role.name for role in admin_roles]
    
    if "管理员" not in admin_role_names and "超级管理员" not in admin_role_names:
        raise HTTPException(status_code=403, detail="只有管理员才能删除用户")
    
    user = user_crud.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 执行软删除（禁用）
    user_crud.update(db, user, {"is_active": False})
    return {"message": "用户已成功禁用", "user_id": user_id}


# 示例接口：用户登录
@router.post("/login", response_model=TokenWithUser, summary="用户登录", description="使用用户名和密码进行身份验证并获取 JWT 令牌")
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="账号或密码错误")
    access_token = create_access_token(data={"sub": user.username})
    user_data = sqlalchemy_to_dict(user, exclude=["password"])
    return {"access_token": access_token, "token_type": "bearer", "user": user_data}


@router.post("/create", response_model=UserRead, summary="创建用户", description="注册新用户，用户名必须唯一")
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # create user via user_crud which hashes password
    existing = db.query(User).filter(User.username == user_in.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")
    user = user_crud.create_user(db, user_in)
    return sqlalchemy_to_dict(user, exclude=["password"])


@router.get('/me', response_model=UserRead, summary="获取当前用户信息", description="基于令牌返回当前登录用户的详细资料")
def read_current_user(current_user: User = Depends(get_current_user)):
    return sqlalchemy_to_dict(current_user, exclude=['password'])


@router.post("/assign_role/{user_id}", summary="分配用户角色", description="为指定用户授予特定角色权限")
def assign_user_role(
    user_id: int = Path(..., description="目标用户ID"), 
    role_id: int = Query(..., description="角色ID"), 
    db: Session = Depends(get_db)
):
    """为用户分配角色"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    result = user_role_crud.assign_role(db, user_id, role_id)
    return {"message": "角色分配成功", "user_id": user_id, "role_id": role_id}


@router.delete("/revoke_role/{user_id}", summary="取消用户角色", description="移除用户已有的某个角色")
def revoke_user_role(
    user_id: int = Path(..., description="目标用户ID"), 
    role_id: int = Query(..., description="要移除的角色ID"), 
    db: Session = Depends(get_db)
):
    """取消用户角色"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    user_role_crud.revoke_role(db, user_id, role_id)
    return {"message": "角色取消成功", "user_id": user_id, "role_id": role_id}


@router.get("/{user_id}/roles", summary="获取用户角色列表", description="查询指定用户关联的所有角色")
def get_user_roles_list(user_id: int = Path(..., description="查询的用户ID"), db: Session = Depends(get_db)):
    """获取用户的所有角色"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    roles = get_user_roles(db, user_id)
    return {"user_id": user_id, "roles": roles}


@router.post("/change-password", response_model=ChangePasswordResponse, summary="修改密码", description="登录用户通过提供旧密码来修改新密码")
def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改当前用户的密码"""
    # 获取最新的用户信息
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise_auth_error("用户不存在")
    
    # 验证旧密码
    if not verify_password(request.old_password, user.password):
        raise_business_error("旧密码错误")
    
    # 验证新密码和确认密码一致性（在 Schema 中已验证，此处再验证一次）
    if request.new_password != request.confirm_password:
        raise_business_error("新密码和确认密码不一致")
    
    # 验证新密码不同于旧密码
    if request.old_password == request.new_password:
        raise_business_error("新密码不能与旧密码相同")
    
    # 更新密码
    hashed_password = get_password_hash(request.new_password)
    user.password = hashed_password
    db.commit()
    db.refresh(user)
    
    return {"success": True, "message": "密码修改成功"}


# ============================================================
# 管理员密码重置
# ============================================================

@router.post("/admin/reset-password/{user_id}", summary="管理员重置密码", description="管理员强行重置指定用户的密码")
def admin_reset_password(
    user_id: int = Path(..., description="目标用户ID"),
    new_password: str = Query(..., description="新生成的密码"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """管理员重置用户密码"""
    # 验证当前用户是否为管理员
    from crud.user_role_crud import user_role_crud
    admin_roles = user_role_crud.get_user_roles(db, current_user.id)
    admin_role_names = [role.name for role in admin_roles]
    
    if "管理员" not in admin_role_names and "超级管理员" not in admin_role_names:
        raise HTTPException(status_code=403, detail="只有管理员才能重置密码")
    
    # 获取目标用户
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 重置密码
    try:
        user_crud.reset_password(db, user_id, new_password)
        return {
            "success": True,
            "message": f"用户 {target_user.username} 的密码已重置",
            "user_id": user_id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"密码重置失败: {str(e)}")


@router.post("/admin/reset-password-by-username", summary="通过用户名重置密码", description="管理员通过用户名强行重置密码")
def admin_reset_password_by_username(
    username: str = Query(..., description="目标用户名"),
    new_password: str = Query(..., description="新生成的密码"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """管理员通过用户名重置密码"""
    # 验证当前用户是否为管理员
    from crud.user_role_crud import user_role_crud
    admin_roles = user_role_crud.get_user_roles(db, current_user.id)
    admin_role_names = [role.name for role in admin_roles]
    
    if "管理员" not in admin_role_names and "超级管理员" not in admin_role_names:
        raise HTTPException(status_code=403, detail="只有管理员才能重置密码")
    
    # 获取目标用户
    target_user = db.query(User).filter(User.username == username).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 重置密码
    try:
        user_crud.reset_password_by_username(db, username, new_password)
        return {
            "success": True,
            "message": f"用户 {username} 的密码已重置",
            "username": username
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"密码重置失败: {str(e)}")
