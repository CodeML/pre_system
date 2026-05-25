"""
客户标签 API 端点
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List
from database.db import get_db
from models.user import User
from config.auth import get_current_user
from crud.customer_tag_crud import customer_tag_crud
from pydantic import BaseModel, Field


# ============= Pydantic Schema =============

class CustomerTagCreate(BaseModel):
    """创建标签请求"""
    name: str = Field(..., description="标签名称")
    description: str = Field(None, description="详细描述")
    category: str = Field(None, description="分类")
    color: str = Field(None, description="显示的十六进制颜色值")


class CustomerTagRead(BaseModel):
    """标签响应"""
    id: int = Field(..., description="标签ID")
    name: str = Field(..., description="标签名称")
    description: str = Field(None, description="描述")
    category: str = Field(None, description="分类")
    color: str = Field(None, description="颜色")
    usage_count: int = Field(0, description="被使用的次数")
    is_active: bool = Field(True, description="是否活跃")

    class Config:
        from_attributes = True


class TagAssignmentRequest(BaseModel):
    """分配标签请求"""
    tag_id: int = Field(..., description="要分配的标签ID")
    remark: str = Field(None, description="关联备注")


class BulkTagAssignmentRequest(BaseModel):
    """批量分配标签请求"""
    tag_ids: List[int] = Field(..., description="标签ID列表")


# ============= 路由 =============

router = APIRouter()


# ============= 标签管理端点 (Tag CRUD) =============
# 路由: /api/customer-tag/tags/*

@router.post("/tags", response_model=CustomerTagRead, summary="创建标签", description="在全局标签库中定义一个新标签，包括名称、分类及显示颜色。")
def create_tag(
    tag_data: CustomerTagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建标签"""
    tag = customer_tag_crud.create(
        db,
        name=tag_data.name,
        description=tag_data.description,
        category=tag_data.category,
        color=tag_data.color,
        creator_id=current_user.id
    )
    return tag


@router.get("/tags/list", response_model=List[CustomerTagRead], summary="获取标签列表", description="分页查询全局标签库中的所有可用标签。")
def get_tags(
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数"),
    is_active: bool = Query(True, description="是否仅看活跃标签"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取标签列表"""
    query = db.query(customer_tag_crud.model)
    if is_active:
        query = query.filter(customer_tag_crud.model.is_active == True)
    tags = query.offset(skip).limit(limit).all()
    return tags


@router.get("/tags/popular", response_model=List[CustomerTagRead], summary="获取热门标签", description="按客户关联的使用频率排序，获取最常用的标签列表。")
def get_popular_tags(
    limit: int = Query(10, ge=1, le=100, description="返回数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取热门标签"""
    tags = customer_tag_crud.get_popular_tags(db, limit=limit)
    return tags


@router.get("/tags/search", response_model=List[CustomerTagRead], summary="搜索标签", description="根据名称关键字模糊搜索全局标签。")
def search_tags(
    q: str = Query(..., min_length=1, description="搜索关键字"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """搜索标签"""
    tags = customer_tag_crud.search_by_name(db, q)
    return tags


@router.get("/tags/category/{category}", response_model=List[CustomerTagRead], summary="按类别获取标签", description="根据业务分类（如：等级、偏好）筛选标签。")
def get_tags_by_category(
    category: str = Path(..., description="类别名称"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按类别获取标签"""
    tags = customer_tag_crud.get_by_category(db, category)
    return tags


@router.get("/tags/{tag_id}", response_model=CustomerTagRead, summary="获取标签详情", description="根据 ID 获取单个标签的配置信息。")
def get_tag(
    tag_id: int = Path(..., description="标签ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取标签详情"""
    tag = customer_tag_crud.get(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    return tag


@router.put("/tags/{tag_id}", response_model=CustomerTagRead, summary="更新标签", description="修改标签的名称、颜色、描述或分类信息。")
def update_tag(
    tag_id: int = Path(..., description="标签ID"),
    tag_data: CustomerTagCreate = Body(..., description="标签更新数据"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新标签"""
    tag = customer_tag_crud.update(
        db,
        tag_id,
        {
            "name": tag_data.name,
            "description": tag_data.description,
            "category": tag_data.category,
            "color": tag_data.color
        }
    )
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    return tag


@router.delete("/tags/{tag_id}", summary="删除标签", description="从全局标签库中永久移除该标签记录。")
def delete_tag(
    tag_id: int = Path(..., description="标签ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除标签"""
    tag = customer_tag_crud.get(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    customer_tag_crud.delete(db, tag_id)
    return {"message": "标签已删除"}


@router.post("/tags/init-predefined", summary="初始化预定义标签", description="管理员一键生成系统内置的推荐标签集合。")
def init_predefined_tags(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """初始化预定义标签"""
    count = customer_tag_crud.create_predefined_tags(db)
    return {"message": f"已创建 {count} 个预定义标签"}


# ============= 客户标签关联端点 (Customer-Tag Association) =============
# 路由: /api/customer-tag/customer/{customer_id}/*

@router.post("/customer/{customer_id}/tags", summary="为客户分配标签", description="将库中的标签关联到特定客户，可附带分配备注。")
def assign_tag_to_customer(
    customer_id: int = Path(..., description="客户ID"),
    request: TagAssignmentRequest = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """为客户分配标签"""
    # 检查客户是否存在
    from crud.customer_crud import customer_crud
    customer = customer_crud.get(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    
    # 检查标签是否存在
    tag = customer_tag_crud.get(db, request.tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    
    # 分配标签
    association = customer_tag_crud.assign_tag_to_customer(
        db,
        customer_id,
        request.tag_id,
        current_user.id,
        request.remark
    )
    
    return {
        "message": "标签分配成功",
        "customer_id": customer_id,
        "tag_id": request.tag_id
    }


@router.post("/customer/{customer_id}/tags/bulk", summary="批量为客户分配标签", description="一次性为某个客户打上多个已有标签。")
def assign_tags_to_customer(
    customer_id: int = Path(..., description="客户ID"),
    request: BulkTagAssignmentRequest = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """批量为客户分配标签"""
    # 检查客户是否存在
    from crud.customer_crud import customer_crud
    customer = customer_crud.get(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    
    # 批量分配
    count = customer_tag_crud.bulk_assign_tags(
        db,
        customer_id,
        request.tag_ids,
        current_user.id
    )
    
    return {
        "message": f"已为客户分配 {count} 个标签",
        "customer_id": customer_id,
        "tag_count": count
    }


@router.get("/customer/{customer_id}/tags", response_model=List[CustomerTagRead], summary="获取客户的所有标签", description="查看特定客户名下的所有已关联标签列表。")
def get_customer_tags(
    customer_id: int = Path(..., description="客户ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取客户的所有标签"""
    from crud.customer_crud import customer_crud
    customer = customer_crud.get(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    
    tags = customer_tag_crud.get_customer_tags(db, customer_id)
    return tags


@router.delete("/customer/{customer_id}/tags/{tag_id}", summary="移除客户的标签", description="解除特定客户与某个标签的关联关系。")
def remove_tag_from_customer(
    customer_id: int = Path(..., description="客户ID"),
    tag_id: int = Path(..., description="标签ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """移除客户的标签"""
    success = customer_tag_crud.remove_tag_from_customer(db, customer_id, tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="标签关联不存在")
    
    return {"message": "标签已移除"}
