from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from database.db import get_db
from crud.role_crud import role_crud
from models.role import Role
from pydantic import BaseModel, Field
from typing import Optional, List


# Pydantic schemas for Role
class RoleBase(BaseModel):
    name: str = Field(..., description="角色显示名称")
    code: str = Field(..., description="角色编码（如：admin, designer）")
    permission: Optional[str] = Field(None, description="权限字符串或JSON列表")
    is_active: bool = Field(True, description="是否启用")


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: int = Field(..., description="角色ID")
    
    class Config:
        from_attributes = True


router = APIRouter()


@router.post("/create", response_model=RoleRead, summary="创建角色", description="在系统中定义一个新的权限角色（如：主设计师、财务）。")
def create_role(
    role_in: RoleCreate,
    db: Session = Depends(get_db)
):
    """创建角色"""
    existing = db.query(Role).filter(
        (Role.name == role_in.name) | (Role.code == role_in.code)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="角色名称或编码已存在")
    
    role = role_crud.create(db, role_in)
    return role


@router.get("/list", response_model=List[RoleRead], summary="获取角色列表", description="查询系统中定义的所有角色及其基本权限信息。")
def list_roles(
    skip: int = Query(0, description="跳过记录数"), 
    limit: int = Query(100, description="返回记录数"), 
    db: Session = Depends(get_db)
):
    """获取角色列表"""
    roles = role_crud.get_all(db, skip=skip, limit=limit)
    return roles


@router.get("/{role_id}", response_model=RoleRead, summary="获取角色详情", description="根据 ID 获取单个角色的详细配置。")
def get_role(
    role_id: int = Path(..., description="角色ID"), 
    db: Session = Depends(get_db)
):
    """获取角色详情"""
    role = role_crud.get(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    return role


@router.put("/{role_id}", response_model=RoleRead, summary="更新角色", description="修改已有角色的名称、编码或权限设置。")
def update_role(
    role_id: int = Path(..., description="角色ID"),
    role_in: RoleCreate = None,
    db: Session = Depends(get_db)
):
    """更新角色"""
    role = role_crud.get(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    # 检查名称/编码是否被其他角色使用
    existing = db.query(Role).filter(
        (Role.name == role_in.name) | (Role.code == role_in.code),
        Role.id != role_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="角色名称或编码已被使用")
    
    role = role_crud.update(db, role, role_in)
    return role


@router.delete("/{role_id}", summary="删除角色", description="从系统中移除该角色。注意：请确保没有用户正在使用该角色。")
def delete_role(
    role_id: int = Path(..., description="角色ID"),
    db: Session = Depends(get_db)
):
    """删除角色"""
    role = role_crud.get(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    role_crud.delete(db, role_id)
    return {"message": "角色删除成功"}
