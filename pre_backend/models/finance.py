from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from models.base import BaseModel
from datetime import datetime


class FinanceRecord(BaseModel):
    """
    财务收支明细
    """
    __tablename__ = "finance_records"

    type = Column(String(20), nullable=False, comment="记录类型（income-收入/expense-支出）")
    category = Column(String(50), nullable=False, comment="收支分类（项目款/外包费/素材购入/提成等）")
    amount = Column(Float, nullable=False, comment="金额")
    record_date = Column(DateTime, default=datetime.utcnow, comment="发生日期")
    
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, comment="关联项目ID")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="经手人/相关人ID")
    
    status = Column(String(20), default="completed", comment="状态（pending/completed/cancelled）")
    remark = Column(String(500), nullable=True, comment="备注")


class ProjectBudget(BaseModel):
    """
    项目预算与成本核算
    """
    __tablename__ = "project_budgets"

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), unique=True, nullable=False, comment="项目ID")
    
    budget_amount = Column(Float, default=0.0, comment="项目预算总额")
    actual_revenue = Column(Float, default=0.0, comment="实际已收金额")
    actual_cost = Column(Float, default=0.0, comment="实际支出总成本")
    estimated_profit = Column(Float, default=0.0, comment="预估利润")
    
    outsourcing_cost = Column(Float, default=0.0, comment="外包成本支出")
    material_cost = Column(Float, default=0.0, comment="素材采购成本")
    commission_cost = Column(Float, default=0.0, comment="人工提成支出")


class Contract(BaseModel):
    """
    合同与报价单管理
    """
    __tablename__ = "contracts"

    contract_no = Column(String(100), unique=True, nullable=False, comment="合同/报价单编号")
    name = Column(String(255), nullable=False, comment="合同名称")
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, comment="关联项目ID")
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="SET NULL"), nullable=True, comment="关联客户ID")
    
    amount = Column(Float, nullable=False, comment="合同金额")
    status = Column(String(50), default="draft", comment="合同状态（草稿/已发/已签/已完成/已作废）")
    
    file_url = Column(String(500), nullable=True, comment="电子档地址")
    sign_date = Column(DateTime, nullable=True, comment="签署日期")
    expiry_date = Column(DateTime, nullable=True, comment="有效期至")


class Invoice(BaseModel):
    """
    发票管理
    """
    __tablename__ = "invoices"

    invoice_no = Column(String(100), unique=True, nullable=False, comment="发票号")
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, comment="关联项目ID")
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="SET NULL"), nullable=True, comment="关联客户ID")
    
    amount = Column(Float, nullable=False, comment="发票金额")
    tax_rate = Column(Float, default=0.0, comment="税率")
    type = Column(String(50), comment="发票类型（普票/专票）")
    
    status = Column(String(20), default="issued", comment="状态（pending/issued/cancelled）")
    issue_date = Column(DateTime, default=datetime.utcnow, comment="开票日期")
    file_url = Column(String(500), nullable=True, comment="发票扫描件/电子发票地址")
