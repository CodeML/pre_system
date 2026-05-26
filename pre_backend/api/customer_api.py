from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from database.db import get_db
from crud.customer_crud import customer_crud
from models.customer import Customer
from models.user import User
from config.auth import get_current_user
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# Pydantic schemas for Customer
class CustomerBase(BaseModel):
    name: str = Field(..., description="客户名称/公司名")
    contact: Optional[str] = Field(None, description="联系人姓名")
    phone: Optional[str] = Field(None, description="联系电话")
    type: Optional[str] = Field("individual", description="客户类型（individual/enterprise）")
    ecommerce_platform: Optional[str] = Field(None, description="主要经营平台（淘宝/京东等）")
    remark: Optional[str] = Field(None, description="备注信息")


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, description="客户名称")
    contact: Optional[str] = Field(None, description="联系人")
    phone: Optional[str] = Field(None, description="联系电话")
    type: Optional[str] = Field(None, description="客户类型")
    ecommerce_platform: Optional[str] = Field(None, description="电商平台")
    remark: Optional[str] = Field(None, description="备注")


class CustomerRead(CustomerBase):
    id: int = Field(..., description="客户ID")
    creator_id: Optional[int] = Field(None, description="创建人ID")
    create_time: Optional[datetime] = Field(None, description="创建时间")
    update_time: Optional[datetime] = Field(None, description="最后更新时间")
    
    class Config:
        from_attributes = True


router = APIRouter()


@router.post("/create", response_model=CustomerRead, summary="创建客户", description="登记新客户信息，系统会自动将当前操作员记录为该客户的创建人。")
def create_customer(
    customer_in: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建客户（自动关联当前登录用户为创建人）"""
    customer = customer_crud.create_customer(db, customer_in, creator_id=current_user.id)
    return customer


@router.get("/list", response_model=List[CustomerRead], summary="获取客户列表", description="分页查询系统中登记的所有客户信息。")
def list_customers(
    skip: int = Query(0, description="跳过记录数"), 
    limit: int = Query(100, description="返回记录数"), 
    db: Session = Depends(get_db)
):
    """获取客户列表"""
    customers = customer_crud.get_all(db, skip=skip, limit=limit)
    return customers


@router.get("/{customer_id}", response_model=CustomerRead, summary="获取客户详情", description="根据 ID 获取单个客户的详细资料。")
def get_customer(
    customer_id: int = Path(..., description="客户ID"), 
    db: Session = Depends(get_db)
):
    """获取客户详情"""
    customer = customer_crud.get(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    return customer


@router.put("/{customer_id}", response_model=CustomerRead, summary="更新客户信息", description="修改客户的联系方式、类型、备注等。仅限该客户的创建人操作。")
def update_customer(
    customer_id: int = Path(..., description="客户ID"),
    customer_in: CustomerUpdate = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新客户信息（仅创建人可编辑）"""
    customer = customer_crud.get(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    
    # 权限检查：仅创建人可编辑
    if customer.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有创建人才能编辑客户信息")
    
    customer = customer_crud.update(db, customer, customer_in)
    return customer


@router.delete("/{customer_id}", summary="删除客户", description="从系统中移除该客户信息。仅限该客户的创建人操作。")
def delete_customer(
    customer_id: int = Path(..., description="客户ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除客户（仅创建人可删除）"""
    customer = customer_crud.get(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    
    # 权限检查：仅创建人可删除
    if customer.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有创建人才能删除客户")
    
    customer_crud.delete(db, customer_id)
    return {"message": "客户删除成功"}


@router.get("/filter/platform/{platform}", response_model=List[CustomerRead], summary="按平台筛选客户", description="筛选在特定电商平台（如：淘宝、抖音）经营的客户。")
def filter_by_platform(
    platform: str = Path(..., description="平台名称"),
    skip: int = Query(0, description="跳过数"),
    limit: int = Query(100, description="返回数"),
    db: Session = Depends(get_db)
):
    """按电商平台筛选客户（支持：淘宝/抖音/小红书/Amazon等）"""
    customers = customer_crud.get_by_ecommerce_platform(db, platform, skip, limit)
    return customers


@router.get("/search/name/{name}", response_model=List[CustomerRead], summary="按名称搜索客户", description="根据客户名称进行模糊匹配查询。")
def search_by_name(
    name: str = Path(..., description="客户名称关键字"),
    skip: int = Query(0, description="跳过数"),
    limit: int = Query(100, description="返回数"),
    db: Session = Depends(get_db)
):
    """按客户名称模糊搜索"""
    customers = customer_crud.search_by_name(db, name, skip, limit)
    return customers


@router.get("/creator/{creator_id}", response_model=List[CustomerRead], summary="按创建人查询客户", description="获取特定设计总监或操作员负责的所有客户列表。")
def get_customers_by_creator(
    creator_id: int = Path(..., description="创建人（用户）ID"),
    skip: int = Query(0, description="跳过数"),
    limit: int = Query(100, description="返回数"),
    db: Session = Depends(get_db)
):
    """获取特定设计总监的所有客户"""
    # 验证创建人是否存在
    creator = db.query(User).filter(User.id == creator_id).first()
    if not creator:
        raise HTTPException(status_code=404, detail="创建人不存在")
    
    customers = customer_crud.get_by_creator(db, creator_id, skip, limit)
    return customers


# ============================================================
# 批量操作与跟进
# ============================================================

@router.post("/batch/create", summary="批量创建客户", description="一次性导入多个客户信息。")
def batch_create_customers(
    customers_in: List[CustomerCreate] = Body(..., description="客户列表"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """批量创建客户"""
    results = []
    for c_in in customers_in:
        c = customer_crud.create_customer(db, c_in, creator_id=current_user.id)
        results.append(c)
    return {"message": f"成功创建 {len(results)} 个客户", "ids": [r.id for r in results]}


@router.put("/batch/update", summary="批量更新客户", description="批量修改客户的标签、归属人等。")
def batch_update_customers(
    customer_ids: List[int] = Body(..., description="客户ID列表"),
    update_data: CustomerUpdate = Body(..., description="更新内容"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """批量更新客户"""
    data = update_data.model_dump(exclude_unset=True)
    count = 0
    for cid in customer_ids:
        c = customer_crud.get(db, cid)
        if c:
            customer_crud.update(db, c, data)
            count += 1
    return {"message": f"成功更新 {count} 个客户"}


@router.get("/statistics", summary="客户数据统计", description="汇总新增、活跃、成交客户等经营指标。")
def get_customer_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取客户统计数据"""
    total = db.query(Customer).count()
    enterprise_count = db.query(Customer).filter(Customer.type == 'enterprise').count()
    return {
        "total_customers": total,
        "enterprise_customers": enterprise_count,
        "individual_customers": total - enterprise_count,
        "active_this_month": total # 简化逻辑
    }


# ============= Schemas for Follow-Up =============
class FollowUpCreate(BaseModel):
    content: str = Field(..., description="跟进内容")
    contact_type: str = Field("微信", description="联系方式")
    next_follow_up_time: Optional[datetime] = None

class FollowUpRead(BaseModel):
    id: int
    content: str
    contact_type: str
    create_time: datetime
    user_id: int
    model_config = ConfigDict(from_attributes=True)


@router.get("/follow-up/{customer_id}", response_model=List[FollowUpRead], summary="获取跟进记录", description="查看与该客户的所有历史商务沟通日志。")
def list_follow_ups(
    customer_id: int = Path(..., description="客户ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """查询客户跟进历史"""
    from models.extra_features import CustomerFollowUp
    return db.query(CustomerFollowUp).filter(CustomerFollowUp.customer_id == customer_id).order_by(CustomerFollowUp.create_time.desc()).all()


@router.post("/follow-up/{customer_id}", response_model=FollowUpRead, summary="新增跟进记录", description="录入一次新的商务洽谈或需求变更沟通记录。")
def create_follow_up(
    customer_id: int = Path(..., description="客户ID"),
    follow_in: FollowUpCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """录入跟进记录"""
    from models.extra_features import CustomerFollowUp
    db_obj = CustomerFollowUp(
        customer_id=customer_id,
        user_id=current_user.id,
        **follow_in.model_dump()
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
