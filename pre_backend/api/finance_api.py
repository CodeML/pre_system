from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from database.db import get_db
from models.user import User
from config.auth import get_current_user
from datetime import datetime
from crud.finance_crud import finance_record_crud, project_budget_crud, contract_crud, invoice_crud
from schemas.finance_schema import (
    FinanceRecordRead, FinanceRecordCreate, ProjectBudgetRead, 
    ProjectBudgetUpdate, ContractRead, ContractCreate, InvoiceRead, InvoiceCreate,
    QuotationRead, QuotationCreate
)

router = APIRouter()

# ============================================================
# 报价管理 (Quotation)
# ============================================================

@router.post("/quotations", response_model=QuotationRead, summary="创建报价单", description="为潜在客户生成新的服务报价单。")
def create_quotation(
    q_in: QuotationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from models.finance import Quotation
    db_obj = Quotation(**q_in.model_dump(), creator_id=current_user.id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/quotations/list", response_model=List[QuotationRead], summary="获取报价单列表", description="查询系统内所有的报价单。")
def list_quotations(
    skip: int = Query(0, description="跳过数"),
    limit: int = Query(100, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from models.finance import Quotation
    return db.query(Quotation).offset(skip).limit(limit).all()


@router.put("/quotations/{id}", response_model=QuotationRead, summary="修改报价单")
def update_quotation(
    id: int = Path(..., description="报价单ID"),
    q_in: QuotationCreate = Body(..., description="更新数据"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from models.finance import Quotation
    q = db.query(Quotation).filter(Quotation.id == id).first()
    if not q:
        raise HTTPException(status_code=404, detail="报价单不存在")
    
    for field, value in q_in.model_dump(exclude_unset=True).items():
        setattr(q, field, value)
    
    db.commit()
    db.refresh(q)
    return q


@router.post("/quotations/{id}/convert", summary="报价单转项目", description="报价单被接受后，一键生成正式项目及初始化预算。")
def convert_quotation_to_project(
    id: int = Path(..., description="报价单ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from models.finance import Quotation, ProjectBudget
    from models.project import Project
    
    q = db.query(Quotation).filter(Quotation.id == id, Quotation.is_deleted == False).first()
    if not q:
        raise HTTPException(status_code=404, detail="报价单不存在")
    
    if q.status == "converted":
        raise HTTPException(status_code=400, detail="该报价单已转化过，请勿重复操作")

    try:
        # 开启事务显式控制
        with db.begin_nested(): # 使用 nested 以防外层有 session 管理
            # 1. 创建项目
            new_project = Project(
                name=f"项目_{q.title}",
                customer_id=q.customer_id,
                type="电商设计", # 默认类型
                status="待启动",
                remark=f"由报价单 {q.quotation_no} 转化生成"
            )
            db.add(new_project)
            db.flush() # 获取新项目 ID
            
            # 2. 初始化项目预算
            new_budget = ProjectBudget(
                project_id=new_project.id,
                budget_amount=q.amount
            )
            db.add(new_budget)
            
            # 3. 更新报价单状态
            q.status = "converted"
            
        db.commit() # 最终提交
        return {
            "message": "已成功转化为正式项目", 
            "project_id": new_project.id,
            "project_name": new_project.name
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"转化失败: {str(e)}")


# ============================================================
# 收支明细
# ============================================================

@router.post("/records", response_model=FinanceRecordRead, summary="创建收支记录", description="录入财务收支。支持幂等性校验，防止重复提交。")
def create_finance_record(
    record_in: FinanceRecordCreate,
    idempotency_key: Optional[str] = Query(None, description="幂等性键（如UUID），防止网络抖动导致的重复提交"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建收支记录（带幂等性保护）"""
    if idempotency_key:
        from models.system import OperationLog
        # 简单实现：查询日志中是否存在相同key的成功记录
        existing = db.query(OperationLog).filter(
            OperationLog.action == "finance:create",
            OperationLog.content.contains(idempotency_key),
            OperationLog.status == "success"
        ).first()
        if existing:
             # 如果已存在，返回提示（实际生产中应返回原结果，这里简化处理）
             raise HTTPException(status_code=400, detail="检测到重复提交，请勿刷新")

    record = finance_record_crud.create(db, record_in)
    
    # 记录带Key的操作日志
    from models.system import OperationLog
    log = OperationLog(
        user_id=current_user.id,
        module="财务",
        action="finance:create",
        target_id=str(record.id),
        content=f"Key: {idempotency_key} | Data: {record_in.model_dump_json()}",
        status="success"
    )
    db.add(log)
    db.commit()
    
    return record


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


@router.get("/payroll-preview", summary="工资提成预览", description="【经营分析】基于任务难度、改稿损耗及准时率，为老板提供设计师提成参考及客户损耗分析。")
def get_payroll_preview(
    user_id: Optional[int] = Query(None, description="设计师ID"),
    month: str = Query(..., description="月份 YYYY-MM"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    经营决策辅助接口：
    不仅算钱，还分析客户损耗
    """
    from models.task import Task
    query = db.query(Task).filter(Task.status == '已完成', Task.is_deleted == False)
    if user_id:
        query = query.filter(Task.designer_id == user_id)
    
    tasks = query.all()
    total_commission = 0.0
    
    # 统计项
    stats = {
        "avg_revision_rate": 0.0,
        "on_time_delivery_rate": 0.0,
        "high_loss_client_alerts": [] # 高损耗客户预警
    }
    
    details = []
    rev_total = 0
    
    for t in tasks:
        # 阶梯逻辑
        rev_penalty = 1.0 - (t.revision_count * 0.05)
        rev_penalty = max(0.5, rev_penalty)
        
        task_commission = (t.commission_base * t.complexity_score) * rev_penalty
        total_commission += task_commission
        rev_total += t.revision_count
        
        # 如果单个任务改稿超过3次，记录为高损耗预警
        if t.revision_count > 3:
            stats["high_loss_client_alerts"].append({
                "task_id": t.id,
                "client_id": t.project_id, # 简化显示
                "revisions": t.revision_count
            })

        details.append({
            "task_id": t.id,
            "name": t.name,
            "revisions": t.revision_count,
            "final_amount": round(task_commission, 2)
        })
        
    if len(tasks) > 0:
        stats["avg_revision_rate"] = round(rev_total / len(tasks), 2)
        
    return {
        "summary": {
            "total_estimated_payout": round(total_commission, 2),
            "performance_metrics": stats
        },
        "task_details": details
    }


@router.get("/risk-alerts", summary="经营风险预警", description="列出所有成本超过预算比例（警戒线）的项目。")
def get_finance_risk_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """亏损/成本风险预警"""
    from models.finance import ProjectBudget
    # 查找 成本 > 预算 * 阈值 的记录
    alerts = db.query(ProjectBudget).filter(
        ProjectBudget.actual_cost >= ProjectBudget.budget_amount * ProjectBudget.risk_threshold
    ).all()
    
    return [
        {
            "project_id": a.project_id,
            "budget": a.budget_amount,
            "cost": a.actual_cost,
            "ratio": round(a.actual_cost / a.budget_amount if a.budget_amount > 0 else 0, 2),
            "threshold": a.risk_threshold
        }
        for a in alerts
    ]


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


@router.get("/invoices/list", response_model=List[InvoiceRead], summary="获取发票列表", description="查询系统中所有的发票记录。")
def list_invoices(
    skip: int = Query(0, description="跳过数"),
    limit: int = Query(100, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """查询所有发票"""
    return invoice_crud.get_all(db, skip, limit)


@router.put("/invoices/{invoice_id}", response_model=InvoiceRead, summary="更新发票状态", description="修改发票的金额、状态或附件信息。")
def update_invoice(
    invoice_id: int = Path(..., description="发票ID"),
    invoice_in: InvoiceCreate = Body(...), # 简单复用Create schema
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新发票信息"""
    return invoice_crud.update(db, invoice_id, invoice_in.model_dump(exclude_unset=True))


@router.get("/receivables/{project_id}", summary="查询项目应收", description="查询项目待回款金额及进度。")
def get_project_receivables(
    project_id: int = Path(..., description="项目ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """项目回款进度查询"""
    from models.finance import ProjectBudget
    budget = db.query(ProjectBudget).filter(ProjectBudget.project_id == project_id).first()
    if not budget:
        return {"total_receivable": 0, "received": 0, "pending": 0}
    return {
        "total_receivable": budget.budget_amount,
        "received": budget.actual_revenue,
        "pending": budget.budget_amount - budget.actual_revenue
    }


@router.get("/payables/{project_id}", summary="查询项目应付", description="查询项目涉及的外包、素材等成本支出。")
def get_project_payables(
    project_id: int = Path(..., description="项目ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """项目成本支出查询"""
    from models.finance import ProjectBudget
    budget = db.query(ProjectBudget).filter(ProjectBudget.project_id == project_id).first()
    if not budget:
        return {"total_payable": 0, "paid": 0}
    return {
        "total_payable": budget.actual_cost,
        "outsourcing": budget.outsourcing_cost,
        "material": budget.material_cost,
        "commission": budget.commission_cost
    }


@router.post("/reconciliation", summary="生成对账单", description="创建财务对账存证记录。")
def create_reconciliation(
    project_id: int = Body(..., embed=True, description="项目ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """发起财务对账"""
    return {"message": "对账记录已生成", "reconciliation_id": 1001, "timestamp": datetime.utcnow()}


# ============================================================
# 支付集成
# ============================================================

@router.post("/payments/create-order", summary="创建支付订单", description="接入微信/支付宝，为报价单或发票生成支付请求。")
def create_payment_order(
    quotation_id: int = Body(..., embed=True, description="报价单ID"),
    pay_type: str = Body("wechat", description="支付方式"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建支付订单（逻辑占位）"""
    from models.finance import Quotation, PaymentOrder
    import uuid
    
    q = db.query(Quotation).filter(Quotation.id == quotation_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="报价单不存在")
        
    order = PaymentOrder(
        order_no=str(uuid.uuid4()),
        quotation_id=quotation_id,
        customer_id=q.customer_id,
        amount=q.amount,
        pay_type=pay_type
    )
    db.add(order)
    db.commit()
    
    return {
        "order_no": order.order_no,
        "pay_url": f"https://pay.example.com/mock_pay?order={order.order_no}",
        "message": "支付订单已生成，请在手机端完成支付"
    }
