from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from database.db import get_db
from config.auth import get_current_user
from models.user import User
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


# ============================================================
# 角色模版与预设
# ============================================================

@router.post("/init-templates", summary="初始化角色模版", description="一键生成 5 个精准业务角色：超管、财务、主管、执行者、客户。")
def init_role_templates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """初始化预设角色及其精细化权限体系"""
    from models.permission import Permission
    
    # 1. 定义全量精细化权限项 (含数据作用域后缀)
    all_perms = [
        # 仪表板
        {"code": "dashboard:view:all", "name": "查看全盘看板"},
        {"code": "dashboard:stats:all", "name": "查看全盘统计"},
        {"code": "dashboard:view:finance", "name": "查看财务看板"},
        {"code": "dashboard:view:production", "name": "查看生产看板"},
        
        # 客户
        {"code": "customer:view:all", "name": "查看所有客户"},
        {"code": "customer:view:limited", "name": "查看限权客户"},
        {"code": "customer:edit:all", "name": "编辑客户信息"},
        {"code": "crm:manage", "name": "线索跟进管理"},
        
        # 项目
        {"code": "project:view:all", "name": "查看所有项目"},
        {"code": "project:view:self", "name": "查看参与的项目"},
        {"code": "project:edit:all", "name": "编辑所有项目"},
        {"code": "project:edit:status", "name": "修改项目状态"},
        {"code": "project:clone", "name": "克隆项目模版"},
        {"code": "project:budget:view", "name": "查看项目利润细节"},
        {"code": "project:budget:view:limited", "name": "仅查看项目成本"},
        
        # 任务
        {"code": "task:view:all", "name": "查看所有任务"},
        {"code": "task:view:self", "name": "查看自己的任务"},
        {"code": "task:edit:all", "name": "编辑所有任务"},
        {"code": "task:edit:self", "name": "执行/编辑自有任务"},
        {"code": "task:assign:all", "name": "任务派发权限"},
        {"code": "task:qc:submit", "name": "提交任务内审"},
        {"code": "task:qc:approve", "name": "审核内审通过"},
        {"code": "task:qc:reject", "name": "内审驳回权"},
        
        # 文件与素材
        {"code": "file:view:all", "name": "查看所有文件"},
        {"code": "file:view:self", "name": "查看关联文件"},
        {"code": "file:edit:all", "name": "管理所有文件"},
        {"code": "file:edit:self", "name": "管理自有文件"},
        {"code": "file:confirm:self", "name": "文件确认(客户)"},
        {"code": "material:view:all", "name": "素材库全看"},
        {"code": "material:edit:all", "name": "素材库管理"},
        {"code": "material:create", "name": "贡献/创建素材"},
        
        # 财务
        {"code": "finance:quote:all", "name": "管理所有报价单"},
        {"code": "finance:quote:view", "name": "查看报价单"},
        {"code": "finance:quote:self", "name": "查看个人报价单"},
        {"code": "finance:transaction:all", "name": "管理所有收支记录"},
        {"code": "finance:invoice:manage", "name": "开票与发票管理"},
        {"code": "finance:contract:all", "name": "管理所有合同"},
        {"code": "finance:contract:view", "name": "查看合同明细"},
        {"code": "finance:payroll:view", "name": "查看提成核算"},
        {"code": "finance:risk:view", "name": "查看成本风险预警"},
        {"code": "finance:reconciliation:all", "name": "执行对账结算"},
        {"code": "finance:pay:self", "name": "在线支付(客户)"},
        
        # 人事与绩效
        {"code": "hr:user:manage", "name": "员工账号管理"},
        {"code": "hr:attendance:manage", "name": "考勤全员管理"},
        {"code": "hr:attendance:view", "name": "查看部门考勤"},
        {"code": "hr:attendance:self", "name": "个人打卡考勤"},
        {"code": "hr:performance:manage", "name": "绩效评分管理"},
        {"code": "hr:performance:view", "name": "查看员工绩效"},
        {"code": "hr:performance:self", "name": "查看个人绩效"},
        {"code": "hr:timesheet:submit", "name": "提交工时记录"},
        
        # 流程与售后
        {"code": "approval:manage", "name": "审批流全局管理"},
        {"code": "aftersale:manage", "name": "售后服务管理"},
        {"code": "aftersale:view", "name": "查看售后记录"},
        {"code": "aftersale:view:self", "name": "查看个人售后"},
        {"code": "aftersale:create:self", "name": "发起售后投诉"},
        
        # 系统
        {"code": "system:role:manage", "name": "角色权限配置"},
        {"code": "system:trash:manage", "name": "回收站管理"},
        {"code": "system:log:view", "name": "审计日志查看"},
        {"code": "system:config:manage", "name": "系统参数配置"}
    ]
    
    perm_objs = {}
    for p in all_perms:
        obj = db.query(Permission).filter(Permission.code == p["code"]).first()
        if not obj:
            obj = Permission(**p)
            db.add(obj)
            db.flush()
        else:
            # 更新已有权限名称，确保描述最新
            obj.name = p["name"]
        perm_objs[p["code"]] = obj

    # 2. 定义 5 大核心角色模板
    templates = [
        {
            "name": "超级管理员", 
            "code": "super_admin", 
            "perms": [p["code"] for p in all_perms]
        },
        {
            "name": "财务", 
            "code": "finance", 
            "perms": [
                "dashboard:view:finance", "customer:view:limited", "project:view:all", 
                "project:budget:view", "finance:quote:view", "finance:transaction:all", 
                "finance:invoice:manage", "finance:contract:view", "finance:payroll:view", 
                "finance:risk:view", "finance:reconciliation:all"
            ]
        },
        {
            "name": "主管", 
            "code": "leader", 
            "perms": [
                "dashboard:view:production", "dashboard:stats:production", "customer:view:limited",
                "project:view:all", "project:edit:status", "project:clone", "task:view:all", 
                "task:edit:all", "task:assign:all", "task:qc:submit", "task:qc:approve", 
                "task:qc:reject", "file:view:all", "material:view:all", "project:budget:view:limited", 
                "hr:performance:view", "hr:attendance:view", "approval:manage", "aftersale:view"
            ]
        },
        {
            "name": "执行者", 
            "code": "executor", 
            "perms": [
                "task:view:self", "task:edit:self", "task:qc:submit", "file:view:self", 
                "file:edit:self", "material:view:all", "material:create", "hr:attendance:self", 
                "hr:performance:self", "hr:timesheet:submit", "aftersale:view:self"
            ]
        },
        {
            "name": "客户", 
            "code": "user", 
            "perms": [
                "project:view:self", "file:view:self", "file:confirm:self", 
                "finance:quote:self", "finance:pay:self", "aftersale:view:self", 
                "aftersale:create:self"
            ]
        }
    ]
    
    for t in templates:
        role = db.query(Role).filter(Role.code == t["code"]).first()
        if not role:
            role = Role(name=t["name"], code=t["code"])
            db.add(role)
            db.flush()
        
        # 强制同步权限
        role.permissions = [perm_objs[p_code] for p_code in t["perms"] if p_code in perm_objs]
    
    db.commit()
    return {"message": f"成功初始化/更新 {len(templates)} 个标准角色模板及精细化权限项"}
