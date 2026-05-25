from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from database.db import get_db
from crud.task_category_crud import task_category_crud
from models.task_category import TaskCategory
from config.auth import get_current_user
from models.user import User
from utils.auth_utils import get_user_role_codes
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Pydantic schemas for TaskCategory
class TaskCategoryBase(BaseModel):
    parent_id: Optional[int] = Field(None, description="父分类ID")
    name: str = Field(..., description="分类名称")
    role_ids: Optional[List[int]] = Field(None, description="可访问该分类的角色ID列表")
    is_ecommerce: Optional[bool] = Field(False, description="是否属于电商设计类")
    params: Optional[dict] = Field(None, description="该分类对应的电商参数模版")
    description: Optional[str] = Field(None, description="详细描述")
    is_active: Optional[bool] = Field(True, description="是否启用")


class TaskCategoryCreate(TaskCategoryBase):
    pass


class TaskCategoryUpdate(BaseModel):
    parent_id: Optional[int] = Field(None, description="父分类ID")
    name: Optional[str] = Field(None, description="分类名称")
    role_ids: Optional[List[int]] = Field(None, description="角色ID列表")
    is_ecommerce: Optional[bool] = Field(None, description="是否电商类")
    params: Optional[dict] = Field(None, description="参数模版")
    description: Optional[str] = Field(None, description="描述")
    is_active: Optional[bool] = Field(None, description="启用状态")


class TaskCategoryRead(TaskCategoryBase):
    id: int = Field(..., description="分类ID")
    create_time: Optional[datetime] = Field(None, description="创建时间")
    update_time: Optional[datetime] = Field(None, description="更新时间")
    
    class Config:
        from_attributes = True


class TaskCategoryTree(BaseModel):
    id: int = Field(..., description="分类ID")
    name: str = Field(..., description="分类名称")
    is_ecommerce: bool = Field(..., description="是否电商类")
    description: Optional[str] = Field(None, description="描述")
    children: Optional[List['TaskCategoryTree']] = Field(None, description="子分类列表")


# 更新转发引用
TaskCategoryTree.model_rebuild()


router = APIRouter()


@router.post("/create", response_model=TaskCategoryRead, summary="创建任务分类", description="定义一个新的任务分类，可设置父分类、适用角色及是否属于电商设计类。")
def create_task_category(
    category_in: TaskCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建任务分类"""
    # 如果指定了父分类，验证它是否存在
    if category_in.parent_id:
        parent = task_category_crud.get(db, category_in.parent_id)
        if not parent:
            raise HTTPException(status_code=404, detail="父分类不存在")
    
    category = task_category_crud.create(db, category_in)
    return category


@router.get("/list", response_model=List[TaskCategoryRead], summary="获取全部分类", description="分页查询系统中定义的所有任务分类。")
def list_task_categories(
    skip: int = Query(0, description="跳过记录数"), 
    limit: int = Query(100, description="返回记录数"), 
    db: Session = Depends(get_db)
):
    """获取所有任务分类"""
    categories = task_category_crud.get_all(db, skip=skip, limit=limit)
    return categories


@router.get("/tree", response_model=List[TaskCategoryTree], summary="获取分类树结构", description="以树形结构返回所有任务分类，方便前端构建级联选择器。")
def get_category_tree(db: Session = Depends(get_db)):
    """获取分类树结构（多级）"""
    tree = task_category_crud.get_tree_structure(db, parent_id=None)
    return tree


@router.get("/{category_id}", response_model=TaskCategoryRead, summary="获取分类详情", description="根据 ID 获取单个分类的详细配置。")
def get_task_category(
    category_id: int = Path(..., description="分类ID"), 
    db: Session = Depends(get_db)
):
    """获取分类详情"""
    category = task_category_crud.get(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    return category


@router.get("/{category_id}/subcategories", response_model=List[TaskCategoryRead], summary="获取子分类", description="查询指定分类下的所有直接子分类列表。")
def get_subcategories(
    category_id: int = Path(..., description="分类ID"),
    skip: int = Query(0, description="跳过数"),
    limit: int = Query(100, description="返回数"),
    db: Session = Depends(get_db)
):
    """获取某个分类的所有子分类"""
    # 验证分类是否存在
    category = task_category_crud.get(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    subcategories = task_category_crud.get_subcategories(db, parent_id=category_id, skip=skip, limit=limit)
    return subcategories


@router.get("/{category_id}/parents", response_model=List[TaskCategoryRead], summary="获取祖先链", description="向上递归查询分类的所有父级，返回完整的路径链。")
def get_parent_categories(
    category_id: int = Path(..., description="分类ID"), 
    db: Session = Depends(get_db)
):
    """获取分类的所有父分类（祖先链）"""
    category = task_category_crud.get(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    parents = task_category_crud.get_parents(db, category_id)
    return parents


@router.put("/{category_id}", response_model=TaskCategoryRead, summary="更新分类信息", description="修改分类的名称、父级关联、角色限制等元数据。")
def update_task_category(
    category_id: int = Path(..., description="分类ID"),
    category_in: TaskCategoryUpdate = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新任务分类"""
    category = task_category_crud.get(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    # 如果修改了父分类，验证新的父分类是否存在
    if category_in.parent_id and category_in.parent_id != category.parent_id:
        parent = task_category_crud.get(db, category_in.parent_id)
        if not parent:
            raise HTTPException(status_code=404, detail="新的父分类不存在")
    
    category = task_category_crud.update(db, category, category_in)
    return category


@router.delete("/{category_id}", summary="删除分类", description="移除指定的任务分类。如果分类下仍有子分类，则拒绝删除。")
def delete_task_category(
    category_id: int = Path(..., description="分类ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除任务分类"""
    category = task_category_crud.get(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    # 检查是否有子分类
    subcategories = task_category_crud.get_subcategories(db, parent_id=category_id)
    if subcategories:
        raise HTTPException(status_code=400, detail="分类下还有子分类，无法删除")
    
    task_category_crud.delete(db, category_id)
    return {"message": "分类删除成功"}


@router.get("/filter/ecommerce", response_model=List[TaskCategoryRead], summary="获取电商分类", description="专门筛选标记为电商设计相关的任务分类。")
def filter_ecommerce_categories(
    skip: int = Query(0, description="跳过数"),
    limit: int = Query(100, description="返回数"),
    db: Session = Depends(get_db)
):
    """获取所有电商设计分类"""
    categories = task_category_crud.get_by_ecommerce(db, skip=skip, limit=limit)
    return categories


@router.get("/filter/my-accessible", response_model=List[TaskCategoryRead], summary="获取可用分类", description="根据当前登录用户的角色，获取其有权操作的任务分类列表。")
def get_accessible_categories(
    skip: int = Query(0, description="跳过数"),
    limit: int = Query(100, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户可操作的分类（按角色筛选）"""
    # 获取用户的所有角色ID
    from models.user_role import UserRole
    user_role_data = db.query(UserRole).filter(UserRole.user_id == current_user.id).all()
    role_ids = [ur.role_id for ur in user_role_data]
    
    if not role_ids:
        # 如果用户没有角色，只能访问没有限制的分类
        categories = db.query(TaskCategory).filter(
            TaskCategory.role_ids == None,
            TaskCategory.is_active == True
        ).offset(skip).limit(limit).all()
    else:
        categories = task_category_crud.get_by_roles(db, role_ids, skip=skip, limit=limit)
    
    return categories


@router.get("/level/{parent_id}", response_model=List[TaskCategoryRead], summary="按层级获取分类", description="获取指定父分类下的同级分类列表。")
def get_categories_by_level(
    parent_id: int = Path(..., description="父分类ID"),
    skip: int = Query(0, description="跳过数"),
    limit: int = Query(100, description="返回数"),
    db: Session = Depends(get_db)
):
    """获取某一级的所有分类"""
    categories = task_category_crud.get_all_by_level(db, parent_id=parent_id)
    return categories[skip:skip + limit]
