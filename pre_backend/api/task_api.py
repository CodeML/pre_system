from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from config.auth import get_current_user
from database.db import get_db
from models.user import User
from models.task import Task
from crud.task_crud import task_crud
from schemas.task_schema import (
    TaskCreate, TaskUpdate, TaskRead, TaskListRead,
    TaskProgressUpdate, ProjectProgressRead
)
from schemas.task_comment_schema import (
    TaskCommentCreate, TaskCommentRead
)
from crud.task_comment_crud import task_comment_crud
from utils.ecommerce_utils import (
    validate_ecommerce_params, get_platform_specs, suggest_params
)

router = APIRouter()


# ============================================================
# 基础 CRUD 操作
# ============================================================

@router.post("/create", response_model=TaskRead, summary="创建任务", description="在指定项目中创建新任务，并关联分类、设计师及设置电商参数。")
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新任务"""
    try:
        # 验证项目是否存在
        from crud.project_crud import project_crud
        project = project_crud.get(db, task_data.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")

        # 如果指定了分类，验证分类是否存在
        if task_data.category_id:
            from crud.task_category_crud import task_category_crud
            category = task_category_crud.get(db, task_data.category_id)
            if not category:
                raise HTTPException(status_code=404, detail="任务分类不存在")

        task = task_crud.create_task(
            db,
            project_id=task_data.project_id,
            category_id=task_data.category_id,
            name=task_data.name,
            designer_id=task_data.designer_id,
            role_ids=task_data.role_ids,
            progress=task_data.progress,
            status=task_data.status,
            ecommerce_params=task_data.ecommerce_params,
            deadline=task_data.deadline,
            priority=task_data.priority,
            description=task_data.description,
            remark=task_data.remark
        )
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"创建任务失败: {str(e)}")


@router.get("/list", response_model=List[TaskListRead], summary="获取任务列表", description="分页查询系统内所有活跃任务。")
def list_tasks(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的最大记录数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务列表"""
    tasks = task_crud.get_list(db, skip=skip, limit=limit)
    return tasks


@router.get("/{task_id}", response_model=TaskRead, summary="获取任务详情", description="根据 ID 获取单个任务的详细信息。")
def get_task(
    task_id: int = Path(..., description="任务ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务详情"""
    task = task_crud.get(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task


@router.put("/{task_id}", response_model=TaskRead, summary="更新任务信息", description="修改任务名称、状态、优先级、负责人等基本信息。")
def update_task(
    task_id: int = Path(..., description="任务ID"),
    task_data: TaskUpdate = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新任务信息"""
    task = task_crud.get(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    # 准备更新数据
    update_data = {}
    if task_data.name is not None:
        update_data['name'] = task_data.name
    if task_data.description is not None:
        update_data['description'] = task_data.description
    if task_data.designer_id is not None:
        update_data['designer_id'] = task_data.designer_id
    if task_data.status is not None:
        update_data['status'] = task_data.status
    if task_data.priority is not None:
        update_data['priority'] = task_data.priority
    if task_data.deadline is not None:
        update_data['deadline'] = task_data.deadline
    if task_data.remark is not None:
        update_data['remark'] = task_data.remark

    updated_task = task_crud.update(db, task_id, update_data)
    return updated_task


@router.delete("/{task_id}", summary="删除任务", description="软删除指定任务（标记为非活跃状态）。")
def delete_task(
    task_id: int = Path(..., description="任务ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除任务（软删除）"""
    task = task_crud.get(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    task_crud.update(db, task_id, {'is_active': False})
    return {"message": "任务已删除"}


# ============================================================
# 批量操作
# ============================================================

@router.post("/batch/update-status", summary="批量更新状态", description="同时更新多个任务的状态（如：全部设为“已完成”）。")
def batch_update_status(
    task_ids: List[int] = Body(..., embed=True, description="任务ID列表"),
    status: str = Body(..., embed=True, description="新状态名称"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """批量更新任务状态"""
    if not task_ids:
        raise HTTPException(status_code=400, detail="任务ID列表不能为空")
    
    result = task_crud.batch_update_status(db, task_ids, status)
    return result


@router.post("/batch/update-priority", summary="批量更新优先级", description="同时修改多个任务的优先级。")
def batch_update_priority(
    task_ids: List[int] = Body(..., embed=True, description="任务ID列表"),
    priority: str = Body(..., embed=True, description="新优先级（低/中/高/紧急）"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """批量更新任务优先级"""
    if not task_ids:
        raise HTTPException(status_code=400, detail="任务ID列表不能为空")
    
    result = task_crud.batch_update_priority(db, task_ids, priority)
    return result


@router.post("/batch/assign-designer", summary="批量分配设计师", description="将一组任务统一分配给某位设计师。")
def batch_assign_designer(
    task_ids: List[int] = Body(..., embed=True, description="任务ID列表"),
    designer_id: int = Body(..., embed=True, description="设计师用户ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """批量分配设计师"""
    if not task_ids:
        raise HTTPException(status_code=400, detail="任务ID列表不能为空")
    
    result = task_crud.batch_assign_designer(db, task_ids, designer_id)
    return result


@router.post("/batch/delete", summary="批量删除任务", description="批量软删除多个任务。")
def batch_delete_tasks(
    task_ids: List[int] = Body(..., embed=True, description="任务ID列表"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """批量删除任务"""
    if not task_ids:
        raise HTTPException(status_code=400, detail="任务ID列表不能为空")
    
    result = task_crud.batch_delete(db, task_ids)
    return result


# ============================================================
# 数据导出
# ============================================================

@router.get("/export/by-project/{project_id}", summary="按项目导出任务", description="导出指定项目下的所有任务数据（返回 JSON 字典）。")
def export_tasks_by_project(
    project_id: int = Path(..., description="项目ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """导出项目的所有任务"""
    tasks_data = task_crud.export_to_dict(db, project_id=project_id)
    if not tasks_data:
        raise HTTPException(status_code=404, detail="项目暂无任务")
    
    return {
        "project_id": project_id,
        "total": len(tasks_data),
        "tasks": tasks_data
    }


@router.post("/export/batch", summary="批量导出任务", description="根据提供的 ID 列表批量导出任务详细数据。")
def export_tasks_batch(
    task_ids: List[int] = Body(..., embed=True, description="任务ID列表"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """批量导出任务"""
    if not task_ids:
        raise HTTPException(status_code=400, detail="任务ID列表不能为空")
    
    tasks_data = task_crud.export_to_dict(db, task_ids=task_ids)
    return {
        "total": len(tasks_data),
        "tasks": tasks_data
    }


@router.get("/export/all", summary="导出所有任务", description="导出系统内所有任务的完整数据。")
def export_all_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """导出所有任务"""
    tasks_data = task_crud.export_to_dict(db)
    return {
        "total": len(tasks_data),
        "tasks": tasks_data
    }


# ============================================================
# 进度和状态管理
# ============================================================

@router.put("/{task_id}/progress", response_model=TaskRead, summary="更新任务进度", description="修改任务的完成百分比（0-100）。")
def update_task_progress(
    task_id: int = Path(..., description="任务ID"),
    progress_data: TaskProgressUpdate = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新任务进度"""
    try:
        task = task_crud.update_progress(db, task_id, progress_data.progress)
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{task_id}/status/{new_status}", summary="更新任务状态", description="修改任务的当前阶段（如：从“进行中”变为“待确认”）。")
def update_task_status(
    task_id: int = Path(..., description="任务ID"),
    new_status: str = Path(..., description="目标状态名称"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新任务状态"""
    try:
        task = task_crud.update_status(db, task_id, new_status)
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        return {"message": f"任务状态已更新为: {new_status}", "task": TaskRead.from_orm(task)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# 高级查询接口
# ============================================================

@router.get("/filter/by-project/{project_id}", response_model=List[TaskListRead], summary="按项目查询任务", description="获取特定项目下的所有任务数据。")
def get_tasks_by_project(
    project_id: int = Path(..., description="项目ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按项目查询任务"""
    tasks = task_crud.get_by_project(db, project_id, skip=skip, limit=limit)
    return tasks


@router.get("/filter/by-category/{category_id}", response_model=List[TaskListRead], summary="按分类查询任务", description="获取特定业务分类下的所有任务。")
def get_tasks_by_category(
    category_id: int = Path(..., description="分类ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按分类查询任务"""
    tasks = task_crud.get_by_category(db, category_id, skip=skip, limit=limit)
    return tasks


@router.get("/filter/by-status/{status}", response_model=List[TaskListRead], summary="按状态查询任务", description="筛选处于特定状态（待开始/进行中等）的任务。")
def get_tasks_by_status(
    status: str = Path(..., description="状态名称"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按状态查询任务"""
    valid_statuses = ["待开始", "进行中", "待确认", "已完成"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"无效的状态。有效值: {', '.join(valid_statuses)}")

    tasks = task_crud.get_by_status(db, status, skip=skip, limit=limit)
    return tasks


@router.get("/filter/by-designer/{designer_id}", response_model=List[TaskListRead], summary="按设计师查询任务", description="查看分配给特定设计师的任务列表。")
def get_tasks_by_designer(
    designer_id: int = Path(..., description="设计师ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按设计师查询任务"""
    tasks = task_crud.get_by_designer(db, designer_id, skip=skip, limit=limit)
    return tasks


@router.get("/filter/by-priority/{priority}", response_model=List[TaskListRead], summary="按优先级查询任务", description="筛选特定优先级（高/紧急等）的任务。")
def get_tasks_by_priority(
    priority: str = Path(..., description="优先级名称"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按优先级查询任务"""
    valid_priorities = ["低", "中", "高", "紧急"]
    if priority not in valid_priorities:
        raise HTTPException(status_code=400, detail=f"无效的优先级。有效值: {', '.join(valid_priorities)}")

    tasks = task_crud.get_by_priority(db, priority, skip=skip, limit=limit)
    return tasks


@router.get("/filter/by-role/{role_id}", response_model=List[TaskListRead], summary="按角色查询任务", description="查询涉及特定工作角色的任务列表。")
def get_tasks_by_role(
    role_id: int = Path(..., description="角色ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按角色查询任务（role_ids 包含该角色）"""
    tasks = task_crud.get_by_role(db, role_id, skip=skip, limit=limit)
    return tasks


@router.post("/filter/advanced", response_model=List[TaskListRead], summary="高级多条件筛选", description="支持项目、分类、状态、优先级、设计师、角色等多维度的组合筛选。")
def filter_tasks_advanced(
    project_id: Optional[int] = Query(None, description="项目ID"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    status: Optional[str] = Query(None, description="状态"),
    priority: Optional[str] = Query(None, description="优先级"),
    designer_id: Optional[int] = Query(None, description="设计师ID"),
    role_id: Optional[int] = Query(None, description="角色ID"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """高级多条件筛选"""
    tasks = task_crud.filter_by_criteria(
        db,
        project_id=project_id,
        category_id=category_id,
        status=status,
        priority=priority,
        designer_id=designer_id,
        role_id=role_id,
        skip=skip,
        limit=limit
    )
    return tasks


# ============================================================
# 设计师和角色管理
# ============================================================

@router.post("/{task_id}/assign-designer/{designer_id}", summary="分配设计师", description="为特定任务指定主设计师。")
def assign_designer(
    task_id: int = Path(..., description="任务ID"),
    designer_id: int = Path(..., description="设计师用户ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """分配设计师"""
    task = task_crud.assign_designer(db, task_id, designer_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    return {"message": "设计师已分配", "task": TaskRead.from_orm(task)}


@router.post("/{task_id}/roles/{role_id}", summary="添加任务角色", description="将特定的工作角色（如：后期、3D）关联到任务中。")
def add_role_to_task(
    task_id: int = Path(..., description="任务ID"),
    role_id: int = Path(..., description="角色ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """添加角色到任务"""
    task = task_crud.add_role(db, task_id, role_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    return {"message": "角色已添加", "task": TaskRead.from_orm(task)}


@router.delete("/{task_id}/roles/{role_id}", summary="移除任务角色", description="从任务的参与角色列表中移除指定角色。")
def remove_role_from_task(
    task_id: int = Path(..., description="任务ID"),
    role_id: int = Path(..., description="角色ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """从任务移除角色"""
    task = task_crud.remove_role(db, task_id, role_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    return {"message": "角色已移除", "task": TaskRead.from_orm(task)}


# ============================================================
# 电商参数管理
# ============================================================

@router.put("/{task_id}/ecommerce-params", response_model=TaskRead, summary="更新电商参数", description="修改任务关联的电商具体规格参数（如：主图尺寸、分辨率）。")
def update_ecommerce_params(
    task_id: int = Path(..., description="任务ID"),
    ecommerce_params: dict = Body(..., description="参数字典"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新任务电商参数"""
    try:
        task = task_crud.update_ecommerce_params(db, task_id, ecommerce_params)
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/ecommerce/validate-params", summary="校验电商参数", description="根据所选平台和图片类型，验证参数是否符合规范。")
def validate_ecommerce_params_endpoint(
    platform: str = Query(..., description="电商平台"),
    ecommerce_params: dict = Body(..., description="参数字典"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """校验电商参数"""
    result = validate_ecommerce_params(platform, ecommerce_params)
    return {
        "platform": platform,
        "valid": result["valid"],
        "errors": result["errors"],
        "warnings": result["errors"] if not result["valid"] else []
    }


@router.get("/ecommerce/specs/{platform}", summary="获取平台规范", description="查询特定电商平台（淘宝、京东等）的设计规格规范。")
def get_ecommerce_specs(
    platform: str = Path(..., description="平台名称"),
    image_type: Optional[str] = Query(None, description="图片类型"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取电商平台规范"""
    specs = get_platform_specs(platform, image_type)
    if "error" in specs:
        raise HTTPException(status_code=400, detail=specs["error"])
    return specs


@router.get("/ecommerce/suggest-params", summary="获取推荐参数", description="基于平台和类型，自动获取推荐的设计参数模版。")
def get_suggested_params(
    platform: str = Query(..., description="电商平台"),
    image_type: str = Query(..., description="图片类型"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取推荐参数"""
    result = suggest_params(platform, image_type)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


# ============================================================
# 特殊查询
# ============================================================

@router.get("/special/overdue-tasks", response_model=List[TaskListRead], summary="获取逾期任务", description="专门筛选当前已超过截止日期且尚未完成的任务。")
def get_overdue_tasks(
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取逾期任务"""
    tasks = task_crud.get_overdue_tasks(db, skip=skip, limit=limit)
    return tasks


@router.get("/special/upcoming-tasks", summary="获取即将到期任务", description="查询未来指定天数内（默认 7 天）即将到期的任务。")
def get_upcoming_tasks(
    days: int = Query(7, ge=1, le=90, description="预测天数"),
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取即将到期的任务"""
    tasks = task_crud.get_upcoming_tasks(db, days=days, skip=skip, limit=limit)
    return tasks


@router.get("/project/{project_id}/progress", response_model=ProjectProgressRead, summary="获取项目整体进度", description="聚合统计特定项目下所有任务的完成比例及状态分布。")
def get_project_progress(
    project_id: int = Path(..., description="项目ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目整体进度"""
    progress = task_crud.get_project_progress(db, project_id)
    return progress


# ============================================================
# 任务评论
# ============================================================


@router.post("/{task_id}/comments", response_model=TaskCommentRead, summary="发表评论", description="在任务下发表评论或回复，支持公开/私密设置。")
def create_task_comment(
    task_id: int = Path(..., description="任务ID"),
    comment: TaskCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建任务评论"""
    # 验证任务存在
    t = task_crud.get(db, task_id)
    if not t:
        raise HTTPException(status_code=404, detail="任务不存在")

    created = task_comment_crud.create_comment(
        db,
        task_id=task_id,
        author_id=current_user.id,
        content=comment.content,
        parent_id=comment.parent_id,
        is_public=comment.is_public
    )
    return created


@router.get("/{task_id}/comments", response_model=List[TaskCommentRead], summary="获取评论列表", description="分页查询任务下的所有讨论记录。")
def list_task_comments(
    task_id: int = Path(..., description="任务ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务的评论列表"""
    t = task_crud.get(db, task_id)
    if not t:
        raise HTTPException(status_code=404, detail="任务不存在")
    comments = task_comment_crud.get_comments_by_task(db, task_id, skip=skip, limit=limit)
    return comments


@router.delete("/{task_id}/comments/{comment_id}", summary="删除评论", description="删除指定的评论。仅限作者或管理员操作。")
def delete_task_comment(
    task_id: int = Path(..., description="任务ID"),
    comment_id: int = Path(..., description="评论ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除任务评论（作者或管理员）"""
    comment = task_comment_crud.get(db, comment_id)
    if not comment or comment.task_id != task_id:
        raise HTTPException(status_code=404, detail="评论不存在")

    # 仅作者或 admin 可删除
    from config.permissions import get_user_roles
    roles = get_user_roles(db, current_user.id)
    role_codes = [r.code if hasattr(r, 'code') else r for r in roles]
    if comment.author_id != current_user.id and 'admin' not in role_codes:
        raise HTTPException(status_code=403, detail="无权删除此评论")

    task_comment_crud.delete_comment(db, comment_id)
    return {"message": "评论已删除"}
