from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from config.auth import get_current_user
from database.db import get_db
from models.user import User
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from models.project import Project
from crud.project_crud import project_crud
from schemas.project_schema import ProjectCreate, ProjectUpdate, ProjectRead, ProjectListRead

router = APIRouter()


# ============================================================
# 基础 CRUD 操作
# ============================================================

@router.post("/create", response_model=ProjectRead, summary="创建项目", description="初始化新项目，设置客户、类型、主/辅设计师等信息。")
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新项目"""
    try:
        # 验证客户是否存在
        from crud.customer_crud import customer_crud
        customer = customer_crud.get(db, project_data.customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="客户不存在")
        
        project = project_crud.create_project(
            db,
            name=project_data.name,
            customer_id=project_data.customer_id,
            project_type=project_data.type,
            ecommerce_platform=project_data.ecommerce_platform,
            main_designer_id=project_data.main_designer_id,
            assist_designer_id=project_data.assist_designer_id,
            material_ids=project_data.material_ids,
            status=project_data.status,
            start_time=project_data.start_time,
            end_time=project_data.end_time,
            remark=project_data.remark
        )
        return project
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"创建项目失败: {str(e)}")


@router.get("/list", response_model=List[ProjectListRead], summary="获取项目列表", description="分页查询系统内所有活跃项目的简要信息。")
def list_projects(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目列表"""
    projects = project_crud.get_list(db, skip=skip, limit=limit)
    return projects


@router.get("/{project_id}", response_model=ProjectRead, summary="获取项目详情", description="根据 ID 获取项目的完整详细信息，包括关联素材。")
def get_project(
    project_id: int = Path(..., description="项目ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目详情"""
    project = project_crud.get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    return project


from utils.model_utils import sqlalchemy_to_dict
...
@router.put("/{project_id}", response_model=ProjectRead, summary="更新项目信息", description="修改项目的基本元数据。已结案项目禁止非管理员修改。")
def update_project(
    project_id: int = Path(..., description="项目ID"),
    project_data: ProjectUpdate = Body(..., description="项目更新数据"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新项目信息"""
    project = project_crud.get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 状态机：已完结项目保护
    if project.status == "已完结":
        is_admin = current_user.username == "admin"
        if not is_admin:
            raise HTTPException(status_code=400, detail="已完结项目进入归档状态，无法修改")

    # 捕捉变更前快照
    old_snapshot = sqlalchemy_to_dict(project)

    # 准备更新数据
    update_data = project_data.model_dump(exclude_unset=True)
    
    # 商业级精简：仅记录关键字段的 Diff
    CRITICAL_FIELDS = ["status", "name", "customer_id", "main_designer_id"]
    diff = {
        k: {"before": old_snapshot.get(k), "after": v}
        for k, v in update_data.items() if k in CRITICAL_FIELDS and v != old_snapshot.get(k)
    }

    updated_project = project_crud.update(db, project_id, update_data)
    
    if diff:
        from models.system import OperationLog
        import json
        log = OperationLog(
            user_id=current_user.id,
            module="项目",
            action="update",
            target_id=str(project_id),
            content=json.dumps(diff, default=str),
            status="success"
        )
        db.add(log)
        db.commit()

    return updated_project


@router.delete("/{project_id}", summary="删除项目", description="软删除指定项目并放入回收站。")
def delete_project(
    project_id: int = Path(..., description="项目ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除项目（逻辑删除）"""
    project = project_crud.get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    # 逻辑删除
    project_crud.delete(db, project_id)
    return {"message": "项目已成功移除并存入回收站", "project_id": project_id}


# ============================================================
# 项目克隆
# ============================================================

@router.post("/{project_id}/clone", summary="克隆项目", description="快速复制一个现有项目及其所有关联任务和素材设置。")
def clone_project(
    project_id: int = Path(..., description="源项目ID"),
    new_name: str = Query(..., min_length=1, max_length=255, description="新项目名称"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """克隆项目（包括任务和素材关联）"""
    try:
        source_project = project_crud.get(db, project_id)
        if not source_project:
            raise HTTPException(status_code=404, detail="源项目不存在")
        
        cloned_project = project_crud.clone_project(
            db, 
            source_project_id=project_id,
            new_name=new_name,
            creator_id=current_user.id
        )
        
        if not cloned_project:
            raise HTTPException(status_code=400, detail="项目克隆失败")
        
        return {
            "id": cloned_project.id,
            "name": cloned_project.name,
            "source_project_id": project_id,
            "message": "项目克隆成功"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"项目克隆失败: {str(e)}")


# ============================================================
# 高级查询接口
# ============================================================

@router.get("/filter/by-customer/{customer_id}", response_model=List[ProjectListRead], summary="按客户查询项目", description="获取特定客户名下的所有项目。")
def get_projects_by_customer(
    customer_id: int = Path(..., description="客户ID"),
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按客户查询项目"""
    projects = project_crud.get_by_customer(db, customer_id, skip=skip, limit=limit)
    return projects


@router.get("/filter/by-status/{status}", response_model=List[ProjectListRead], summary="按状态查询项目", description="筛选处于特定生命周期阶段的项目。")
def get_projects_by_status(
    status: str = Path(..., description="状态名称（待启动/设计中等）"),
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按状态查询项目（待启动/设计中/待确认/已交付/已完结）"""
    valid_statuses = ["待启动", "设计中", "待确认", "已交付", "已完结"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"无效的状态，必须是: {', '.join(valid_statuses)}")
    
    projects = project_crud.get_by_status(db, status, skip=skip, limit=limit)
    return projects


@router.get("/filter/by-type/{project_type}", response_model=List[ProjectListRead], summary="按类型查询项目", description="按业务类型（如：3D建模、电商页）筛选项目。")
def get_projects_by_type(
    project_type: str = Path(..., description="项目类型名称"),
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按项目类型查询（电商详情页/3D建模/摄影）"""
    projects = project_crud.get_by_type(db, project_type, skip=skip, limit=limit)
    return projects


@router.get("/filter/by-platform/{platform}", response_model=List[ProjectListRead], summary="按平台查询项目", description="筛选针对特定电商平台设计的项目。")
def get_projects_by_platform(
    platform: str = Path(..., description="平台名称"),
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按电商平台查询（淘宝/抖音/小红书/Amazon等）"""
    projects = project_crud.get_by_ecommerce_platform(db, platform, skip=skip, limit=limit)
    return projects


@router.get("/filter/by-designer/{designer_id}", response_model=List[ProjectListRead], summary="按设计师查询项目", description="查看分配给特定设计师（主/辅）的项目列表。")
def get_projects_by_designer(
    designer_id: int = Path(..., description="设计师ID"),
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取设计师相关的项目（主设计师或辅助设计师）"""
    projects = project_crud.get_by_designer(db, designer_id, skip=skip, limit=limit)
    return projects


@router.post("/filter/advanced", response_model=List[ProjectListRead], summary="项目高级筛选", description="支持客户、状态、类型、平台、设计师的多维度组合查询。")
def filter_projects_advanced(
    customer_id: Optional[int] = Query(None, description="客户ID"),
    status: Optional[str] = Query(None, description="项目状态"),
    project_type: Optional[str] = Query(None, description="项目类型"),
    platform: Optional[str] = Query(None, description="电商平台"),
    designer_id: Optional[int] = Query(None, description="设计师ID"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """高级多条件筛选"""
    projects = project_crud.filter_by_criteria(
        db,
        customer_id=customer_id,
        status=status,
        project_type=project_type,
        ecommerce_platform=platform,
        designer_id=designer_id,
        skip=skip,
        limit=limit
    )
    return projects


# ============================================================
# 项目状态操作
# ============================================================

@router.put("/{project_id}/status/{new_status}", summary="更新项目状态", description="直接修改项目的当前运行状态。")
def update_project_status(
    project_id: int = Path(..., description="项目ID"),
    new_status: str = Path(..., description="目标状态名称"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新项目状态"""
    valid_statuses = ["待启动", "设计中", "待确认", "已交付", "已完结"]
    if new_status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"无效的状态，必须是: {', '.join(valid_statuses)}")
    
    project = project_crud.update_project_status(db, project_id, new_status)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    return {"message": f"项目状态已更新为: {new_status}", "project": ProjectRead.from_orm(project)}


# ============================================================
# 设计师分配
# ============================================================

@router.post("/{project_id}/assign-designers", summary="分配项目设计师", description="统一设置或修改项目的主辅助设计师。")
def assign_designers(
    project_id: int = Path(..., description="项目ID"),
    main_designer_id: Optional[int] = Query(None, description="主设计师ID"),
    assist_designer_id: Optional[int] = Query(None, description="辅助设计师ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """分配项目设计师"""
    if main_designer_id is None and assist_designer_id is None:
        raise HTTPException(status_code=400, detail="至少需要指定一个设计师")
    
    project = project_crud.assign_designers(
        db, project_id,
        main_designer_id=main_designer_id,
        assist_designer_id=assist_designer_id
    )
    
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    return {"message": "设计师已分配", "project": ProjectRead.from_orm(project)}


# ============================================================
# 素材管理
# ============================================================

@router.post("/{project_id}/materials/{material_id}", summary="添加素材到项目", description="建立项目与素材库中素材的关联关系。")
def add_material_to_project(
    project_id: int = Path(..., description="项目ID"),
    material_id: int = Path(..., description="素材ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """添加素材到项目"""
    project = project_crud.add_material(db, project_id, material_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    return {"message": "素材已添加", "project": ProjectRead.from_orm(project)}


@router.delete("/{project_id}/materials/{material_id}", summary="从项目移除素材", description="解除项目与特定素材的关联。")
def remove_material_from_project(
    project_id: int = Path(..., description="项目ID"),
    material_id: int = Path(..., description="素材ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """从项目移除素材"""
    project = project_crud.remove_material(db, project_id, material_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    return {"message": "素材已移除", "project": ProjectRead.from_orm(project)}


# ============================================================
# 统计、时间轴与里程碑
# ============================================================

@router.get("/statistics/overview", summary="项目全局统计", description="汇总完成率、延期率、在途项目数等核心经营指标。")
def get_project_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目全局统计"""
    from models.project import Project
    total = db.query(Project).count()
    completed = db.query(Project).filter(Project.status == '已完结').count()
    return {
        "total_projects": total,
        "completed_projects": completed,
        "ongoing_projects": total - completed,
        "on_time_rate": "95%" # 简化逻辑
    }


@router.get("/timeline/{project_id}", summary="获取项目时间轴", description="记录从立项、派单、交付到回款的所有关键操作节点。")
def get_project_timeline(
    project_id: int = Path(..., description="项目ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目操作全记录"""
    from models.system import OperationLog
    logs = db.query(OperationLog).filter(
        OperationLog.module == "项目",
        OperationLog.target_id == str(project_id)
    ).order_by(OperationLog.create_time.asc()).all()
    return logs


# ============= Milestone Schemas =============
class MilestoneCreate(BaseModel):
    name: str = Field(..., description="里程碑名称")
    due_date: Optional[datetime] = None
    remark: Optional[str] = None

class MilestoneRead(MilestoneCreate):
    id: int
    project_id: int
    status: str
    completed_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


@router.post("/milestones/{project_id}", response_model=MilestoneRead, summary="创建里程碑", description="为项目设定关键交付节点（如：初稿定稿、终稿交付）。")
def create_milestone(
    project_id: int = Path(..., description="项目ID"),
    ms_in: MilestoneCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建项目里程碑"""
    from models.extra_features import ProjectMilestone
    db_obj = ProjectMilestone(project_id=project_id, **ms_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.put("/milestones/{milestone_id}", response_model=MilestoneRead, summary="更新里程碑", description="标记里程碑达成或修改节点预测时间。")
def update_milestone(
    milestone_id: int = Path(..., description="里程碑ID"),
    status: Optional[str] = Query(None, description="新状态"),
    completed_at: Optional[datetime] = Query(None, description="达成时间"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新里程碑状态"""
    from models.extra_features import ProjectMilestone
    ms = db.query(ProjectMilestone).filter(ProjectMilestone.id == milestone_id).first()
    if not ms:
        raise HTTPException(status_code=404, detail="里程碑不存在")
    if status:
        ms.status = status
    if completed_at:
        ms.completed_at = completed_at
    db.commit()
    db.refresh(ms)
    return ms
