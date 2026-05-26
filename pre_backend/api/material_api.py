from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List
from config.auth import get_current_user
from database.db import get_db
from models.user import User
from models.material import Material
from crud.material_crud import material_crud
from schemas.material_schema import MaterialCreate, MaterialRead, MaterialUpdate

router = APIRouter()


@router.post("/create", response_model=MaterialRead, summary="创建素材", description="向素材库添加新素材，包含名称、类型、URL 及标签等信息。")
def create_material(
    material_data: MaterialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建素材"""
    material = material_crud.create_material(
        db,
        name=material_data.name,
        type=material_data.type,
        url=material_data.url,
        category=material_data.category,
        file_format=material_data.file_format,
        size=material_data.size,
        uploader_id=current_user.id,
        is_reusable=material_data.is_reusable,
        tags=material_data.tags,
        description=material_data.description
    )
    return material


@router.get("/list", response_model=List[MaterialRead], summary="获取素材列表", description="分页获取素材库中所有活跃素材。")
def list_materials(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取素材列表"""
    materials = material_crud.get_list(db, skip=skip, limit=limit)
    return materials


@router.get("/statistics", summary="获取素材统计", description="获取素材库的总量、分类分布等统计信息。")
def get_material_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取素材库统计"""
    stats = material_crud.get_material_stats(db)
    return stats


@router.get("/filter/popular", summary="获取热门素材", description="按复用次数排序，获取最常用的素材列表。")
def get_popular_materials(
    limit: int = Query(10, ge=1, le=100, description="返回数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取热门素材"""
    materials = material_crud.get_popular_materials(db, limit=limit)
    return [
        {
            "id": m.id,
            "name": m.name,
            "type": m.type,
            "reuse_count": m.reuse_count,
            "url": m.url
        }
        for m in materials
    ]


@router.get("/filter/reusable", response_model=List[MaterialRead], summary="获取可复用素材", description="筛选标记为可重复使用的素材。")
def get_reusable_materials(
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取可复用素材"""
    materials = material_crud.get_reusable(db, skip=skip, limit=limit)
    return materials


@router.get("/filter/by-type/{material_type}", response_model=List[MaterialRead], summary="按类型筛选素材", description="根据素材类型（如：图片、视频、模型）进行筛选。")
def get_materials_by_type(
    material_type: str = Path(..., description="素材类型"),
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按类型查询素材"""
    materials = material_crud.get_by_type(db, material_type, skip=skip, limit=limit)
    return materials


@router.get("/filter/by-category/{category}", response_model=List[MaterialRead], summary="按分类筛选素材", description="按业务分类筛选素材。")
def get_materials_by_category(
    category: str = Path(..., description="分类名称"),
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按分类查询素材"""
    materials = material_crud.get_by_category(db, category, skip=skip, limit=limit)
    return materials


@router.get("/filter/by-tag/{tag}", response_model=List[MaterialRead], summary="按标签筛选素材", description="获取带有特定标签的素材。")
def get_materials_by_tag(
    tag: str = Path(..., description="标签名称"),
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按标签查询素材"""
    materials = material_crud.get_by_tag(db, tag, skip=skip, limit=limit)
    return materials


@router.get("/filter/by-project/{project_id}", response_model=List[MaterialRead], summary="按项目筛选素材", description="查询特定项目已关联的所有素材。")
def get_materials_by_project(
    project_id: int = Path(..., description="项目ID"),
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目关联的素材"""
    materials = material_crud.get_by_project(db, project_id, skip=skip, limit=limit)
    return materials


@router.get("/filter/by-task/{task_id}", response_model=List[MaterialRead], summary="按任务筛选素材", description="查询特定任务已关联的所有素材。")
def get_materials_by_task(
    task_id: int = Path(..., description="任务ID"),
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务关联的素材"""
    materials = material_crud.get_by_task(db, task_id, skip=skip, limit=limit)
    return materials


# ============================================================
# AI 增强功能
# ============================================================

@router.get("/search/semantic", response_model=List[MaterialRead], summary="素材语义搜索", description="【AI增强】通过自然语言描述（如：搜一张简约风背景）搜索素材库。")
def semantic_search_materials(
    q: str = Query(..., description="搜索描述文本"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """语义搜索（逻辑占位）"""
    # 实际应接入向量数据库，这里暂时退化为关键词搜索
    return material_crud.search_by_name(db, q)


@router.get("/{material_id}", response_model=MaterialRead, summary="获取素材详情", description="根据 ID 获取单个素材的详细信息。")
def get_material(
    material_id: int = Path(..., description="素材ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取素材详情"""
    material = material_crud.get(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="素材不存在")
    return material


@router.post("/{material_id}/tasks/{task_id}", summary="关联素材到任务", description="将库中的素材分配给特定的工作任务。")
def add_task_to_material(
    material_id: int = Path(..., description="素材ID"),
    task_id: int = Path(..., description="任务ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """关联素材到任务"""
    try:
        material = material_crud.add_task(db, material_id, task_id)
        if not material:
            raise HTTPException(status_code=404, detail="素材不存在")
        return {"message": "任务关联已添加", "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{material_id}/tasks/{task_id}", summary="移除任务关联", description="解除素材与任务之间的关联关系。")
def remove_task_from_material(
    material_id: int = Path(..., description="素材ID"),
    task_id: int = Path(..., description="任务ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """移除素材与任务的关联"""
    try:
        material = material_crud.remove_task(db, material_id, task_id)
        if not material:
            raise HTTPException(status_code=404, detail="素材不存在")
        return {"message": "任务关联已移除", "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.post("/{material_id}/tags/{tag}", summary="添加素材标签", description="为素材打上新的分类标签。")
def add_tag_to_material(
    material_id: int = Path(..., description="素材ID"),
    tag: str = Path(..., description="标签名称"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """为素材添加标签"""
    try:
        material = material_crud.add_tag(db, material_id, tag)
        if not material:
            raise HTTPException(status_code=404, detail="素材不存在")
        return {"message": "标签已添加"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{material_id}/tags/{tag}", summary="删除素材标签", description="移除素材已有的某个标签。")
def remove_tag_from_material(
    material_id: int = Path(..., description="素材ID"),
    tag: str = Path(..., description="标签名称"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除素材标签"""
    try:
        material = material_crud.remove_tag(db, material_id, tag)
        if not material:
            raise HTTPException(status_code=404, detail="素材不存在")
        return {"message": "标签已删除"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{material_id}/use", summary="记录素材使用", description="手动增加素材的复用计数。")
def increment_material_reuse(
    material_id: int = Path(..., description="素材ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """记录素材使用次数"""
    try:
        material = material_crud.increment_reuse_count(db, material_id)
        if not material:
            raise HTTPException(status_code=404, detail="素材不存在")
        return {"message": "复用计数已更新", "reuse_count": material.reuse_count}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{material_id}", response_model=MaterialRead, summary="更新素材", description="修改素材的基本元数据（名称、分类、描述等）。")
def update_material(
    material_id: int = Path(..., description="素材ID"),
    material_data: MaterialUpdate = Body(..., description="素材更新数据"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    """更新素材"""
    material = material_crud.get(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="素材不存在")

    update_data = material_data.model_dump(exclude_unset=True)
    material = material_crud.update(db, material_id, update_data)
    return material



@router.delete("/{material_id}", summary="删除素材", description="软删除素材库中的素材。")
def delete_material(
    material_id: int = Path(..., description="素材ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除素材"""
    material = material_crud.get(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="素材不存在")
    
    material_crud.update(db, material_id, {'is_active': False})
    return {"message": "素材已删除"}
