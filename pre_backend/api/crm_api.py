from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from database.db import get_db
from models.user import User
from config.auth import get_current_user
from crud.crm_crud import sales_lead_crud, design_package_crud, case_work_crud
from schemas.crm_schema import (
    SalesLeadRead, SalesLeadCreate, 
    DesignPackageRead, DesignPackageCreate, 
    CaseWorkRead, CaseWorkCreate
)

router = APIRouter()

# ============================================================
# 销售线索 (CRM)
# ============================================================

@router.post("/leads", response_model=SalesLeadRead, summary="创建线索", description="登记新的销售线索或意向客户。")
def create_lead(
    lead_in: SalesLeadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建销售线索"""
    return sales_lead_crud.create(db, lead_in)


@router.get("/leads/list", response_model=List[SalesLeadRead], summary="获取线索列表", description="分页查询系统内所有的销售线索。")
def list_leads(
    skip: int = Query(0, description="跳过数"),
    limit: int = Query(100, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """查询销售线索列表"""
    return sales_lead_crud.get_all(db, skip, limit)


# ============================================================
# 设计套餐 (Marketing)
# ============================================================

@router.get("/packages/active", response_model=List[DesignPackageRead], summary="获取上架套餐", description="查询当前所有在售的设计服务套餐。")
def list_active_packages(
    db: Session = Depends(get_db)
):
    """获取活动套餐列表"""
    return design_package_crud.get_active(db)


# ============================================================
# 案例作品 (Marketing)
# ============================================================

@router.post("/cases", response_model=CaseWorkRead, summary="收录案例", description="将优秀的完成项目收录进作品集。")
def create_case(
    case_in: CaseWorkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建案例"""
    return case_work_crud.create(db, case_in)


@router.get("/cases/public", response_model=List[CaseWorkRead], summary="获取公开案例", description="获取对外展示的优秀设计案例。")
def list_public_cases(
    db: Session = Depends(get_db)
):
    """获取公开案例作品"""
    return case_work_crud.get_public(db)
