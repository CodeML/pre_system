from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, JSON, Text
from models.base import BaseModel
from datetime import datetime


class Quotation(BaseModel):
    """
    报价单模型
    """
    __tablename__ = "quotations"

    quotation_no = Column(String(100), unique=True, nullable=False, comment="报价单编号")
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, comment="客户ID")
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="创建人ID")
    
    title = Column(String(255), nullable=False, comment="报价单标题")
    amount = Column(Float, nullable=False, comment="总金额")
    items = Column(JSON, nullable=True, comment="报价明细清单")
    
    status = Column(String(20), default="draft", comment="状态（draft/sent/accepted/rejected/converted）")
    remark = Column(Text, nullable=True)
    file_url = Column(String(500), nullable=True, comment="报价单文件地址")
    
    expiry_date = Column(DateTime, nullable=True, comment="有效期至")


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
    
    # 风险预警
    risk_threshold = Column(Float, default=0.8, comment="成本警戒比例（如0.8表示成本达到预算80%即预警）")
    is_risk_alert = Column(Boolean, default=False, comment="是否处于风险预警状态")
    
    outsourcing_cost = Column(Float, default=0.0, comment="外包成本支出")
    material_cost = Column(Float, default=0.0, comment="素材采购成本")
    commission_cost = Column(Float, default=0.0, comment="人工提成支出")


class PaymentOrder(BaseModel):
    """
    第三方支付订单（微信/支付宝等）
    """
    __tablename__ = "payment_orders"

    order_no = Column(String(100), unique=True, nullable=False)
    quotation_id = Column(Integer, ForeignKey("quotations.id"), nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    
    amount = Column(Float, nullable=False)
    pay_type = Column(String(20), comment="wechat/alipay")
    
    status = Column(String(20), default="pending", comment="pending/paid/failed")
    transaction_id = Column(String(255), nullable=True, comment="第三方流水号")
    pay_time = Column(DateTime, nullable=True)


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


class ChangeRequest(BaseModel):
    """
    需求变更申请（防需求漂移的核心防火墙）
    """
    __tablename__ = "change_requests"

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False, comment="变更项名称")
    reason = Column(Text, nullable=True, comment="变更原因")
    
    # 影响评估
    estimated_hours = Column(Float, default=0, comment="预计增加工时")
    additional_fee = Column(Float, default=0, comment="建议加收费用")
    
    status = Column(String(20), default="pending", comment="pending/approved/rejected")
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
