from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class FinanceRecordBase(BaseModel):
    type: str = Field(..., description="记录类型（income-收入/expense-支出）")
    category: str = Field(..., description="收支分类")
    amount: float = Field(..., description="金额")
    record_date: Optional[datetime] = Field(None, description="发生日期")
    project_id: Optional[int] = Field(None, description="关联项目ID")
    user_id: Optional[int] = Field(None, description="经手人ID")
    status: str = Field("completed", description="状态")
    remark: Optional[str] = Field(None, description="备注")


class FinanceRecordCreate(FinanceRecordBase):
    pass


class FinanceRecordRead(FinanceRecordBase):
    id: int
    create_time: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ProjectBudgetBase(BaseModel):
    project_id: int
    budget_amount: float = 0.0
    actual_revenue: float = 0.0
    actual_cost: float = 0.0
    estimated_profit: float = 0.0
    outsourcing_cost: float = 0.0
    material_cost: float = 0.0
    commission_cost: float = 0.0


class ProjectBudgetUpdate(BaseModel):
    budget_amount: Optional[float] = None
    actual_revenue: Optional[float] = None
    actual_cost: Optional[float] = None
    estimated_profit: Optional[float] = None


class ProjectBudgetRead(ProjectBudgetBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ContractBase(BaseModel):
    contract_no: str = Field(..., description="合同编号")
    name: str = Field(..., description="合同名称")
    project_id: Optional[int] = None
    customer_id: Optional[int] = None
    amount: float = Field(..., description="合同金额")
    status: str = Field("draft", description="合同状态")
    file_url: Optional[str] = None
    sign_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None


class ContractCreate(ContractBase):
    pass


class ContractRead(ContractBase):
    id: int
    create_time: datetime
    model_config = ConfigDict(from_attributes=True)


class InvoiceBase(BaseModel):
    invoice_no: str = Field(..., description="发票号")
    project_id: Optional[int] = None
    customer_id: Optional[int] = None
    amount: float = Field(..., description="发票金额")
    tax_rate: float = 0.0
    type: str = Field(..., description="发票类型")
    status: str = "issued"
    issue_date: Optional[datetime] = None
    file_url: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceRead(InvoiceBase):
    id: int
    create_time: datetime
    model_config = ConfigDict(from_attributes=True)


# ============= Quotation =============
class QuotationBase(BaseModel):
    quotation_no: str = Field(..., description="报价单编号")
    customer_id: int = Field(..., description="客户ID")
    title: str = Field(..., description="标题")
    amount: float = Field(..., description="总金额")
    items: Optional[List[dict]] = Field(None, description="报价项列表")
    remark: Optional[str] = Field(None, description="备注")
    status: str = Field("draft", description="状态")
    expiry_date: Optional[datetime] = Field(None, description="有效期")

class QuotationCreate(QuotationBase):
    pass

class QuotationRead(QuotationBase):
    id: int
    creator_id: int
    create_time: datetime
    model_config = ConfigDict(from_attributes=True)
