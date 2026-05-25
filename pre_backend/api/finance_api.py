from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from database.db import get_db
from models.user import User
from config.auth import get_current_user
from crud.finance_crud import finance_record_crud, project_budget_crud, contract_crud, invoice_crud
from schemas.finance_schema import (
    FinanceRecordRead, FinanceRecordCreate, ProjectBudgetRead, 
    ProjectBudgetUpdate, ContractRead, ContractCreate, InvoiceRead, InvoiceCreate
)

router = APIRouter()

# ============================================================
# 收支明细
# ============================================================

@router.post("/records", response_model=FinanceRecordRead, summary="创建收支记录", description="录入一笔新的财务收支，支持关联项目和人员。")
def create_finance_record(
    record_in: FinanceRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建收支记录"""
    return finance_record_crud.create(db, record_in)


@router.get("/records/list", response_model=List[FinanceRecordRead], summary="获取收支列表", description="分页查询财务收支明细。")
def list_finance_records(
    skip: int = Query(0, description="跳过记录数"),
    limit: int = Query(100, description="返回记录数"),
    project_id: Optional[int] = Query(None, description="关联项目ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取收支记录列表"""
    if project_id:
        return finance_record_crud.get_by_project(db, project_id, skip, limit)
    return finance_record_crud.get_all(db, skip, limit)


@router.get("/summary", summary="获取财务汇总", description="获取总收入、总支出及净利润汇总。")
def get_finance_summary(
    project_id: Optional[int] = Query(None, description="按项目筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """财务汇总统计"""
    return finance_record_crud.get_summary(db, project_id)


# ============================================================
# 项目预算与成本
# ============================================================

@router.get("/budgets/{project_id}", response_model=ProjectBudgetRead, summary="获取项目预算", description="查询特定项目的成本预算及利润核算情况。")
def get_project_budget(
    project_id: int = Path(..., description="项目ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目预算"""
    budget = project_budget_crud.get_by_project(db, project_id)
    if not budget:
        # 如果不存在则初始化一个
        from models.finance import ProjectBudget
        budget = ProjectBudget(project_id=project_id)
        db.add(budget)
        db.commit()
        db.refresh(budget)
    return budget


@router.put("/budgets/{project_id}", response_model=ProjectBudgetRead, summary="更新项目预算", description="修改项目的预算、实际收入或成本。")
def update_project_budget(
    project_id: int = Path(..., description="项目ID"),
    budget_in: ProjectBudgetUpdate = Body(..., description="预算更新数据"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新项目预算"""
    budget = project_budget_crud.get_by_project(db, project_id)
    if not budget:
        raise HTTPException(status_code=404, detail="项目预算记录不存在")
    
    update_data = budget_in.model_dump(exclude_unset=True)
    return project_budget_crud.update(db, budget.id, update_data)


# ============================================================
# 合同管理
# ============================================================

@router.post("/contracts", response_model=ContractRead, summary="创建合同", description="登记一份新的报价单或合同信息。")
def create_contract(
    contract_in: ContractCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建合同"""
    return contract_crud.create(db, contract_in)


@router.get("/contracts/project/{project_id}", response_model=List[ContractRead], summary="按项目获取合同", description="查询指定项目下的所有合同记录。")
def list_project_contracts(
    project_id: int = Path(..., description="项目ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目关联的合同"""
    return contract_crud.get_by_project(db, project_id)


# ============================================================
# 发票管理
# ============================================================

@router.post("/invoices", response_model=InvoiceRead, summary="创建发票记录", description="录入开票明细。")
def create_invoice(
    invoice_in: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建发票"""
    return invoice_crud.create(db, invoice_in)
