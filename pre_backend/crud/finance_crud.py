from crud.base_crud import BaseCRUD
from models.finance import FinanceRecord, ProjectBudget, Contract, Invoice
from sqlalchemy.orm import Session
from sqlalchemy import func


class FinanceRecordCRUD(BaseCRUD):
    def get_by_project(self, db: Session, project_id: int, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(self.model.project_id == project_id).offset(skip).limit(limit).all()

    def get_summary(self, db: Session, project_id: int = None):
        """获取财务汇总"""
        query = db.query(
            func.sum(self.model.amount).filter(self.model.type == 'income').label('total_income'),
            func.sum(self.model.amount).filter(self.model.type == 'expense').label('total_expense')
        )
        if project_id:
            query = query.filter(self.model.project_id == project_id)
        
        result = query.first()
        return {
            "total_income": result.total_income or 0.0,
            "total_expense": result.total_expense or 0.0,
            "net_profit": (result.total_income or 0.0) - (result.total_expense or 0.0)
        }


class ProjectBudgetCRUD(BaseCRUD):
    def get_by_project(self, db: Session, project_id: int):
        return db.query(self.model).filter(self.model.project_id == project_id).first()


class ContractCRUD(BaseCRUD):
    def get_by_project(self, db: Session, project_id: int):
        return db.query(self.model).filter(self.model.project_id == project_id).all()


class InvoiceCRUD(BaseCRUD):
    def get_by_project(self, db: Session, project_id: int):
        return db.query(self.model).filter(self.model.project_id == project_id).all()


finance_record_crud = FinanceRecordCRUD(FinanceRecord)
project_budget_crud = ProjectBudgetCRUD(ProjectBudget)
contract_crud = ContractCRUD(Contract)
invoice_crud = InvoiceCRUD(Invoice)
