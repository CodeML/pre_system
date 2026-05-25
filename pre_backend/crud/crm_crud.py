from crud.base_crud import BaseCRUD
from models.crm import SalesLead, DesignPackage, CaseWork
from sqlalchemy.orm import Session


class SalesLeadCRUD(BaseCRUD):
    pass


class DesignPackageCRUD(BaseCRUD):
    def get_active(self, db: Session):
        return db.query(self.model).filter(self.model.is_active == True).all()


class CaseWorkCRUD(BaseCRUD):
    def get_public(self, db: Session):
        return db.query(self.model).filter(self.model.is_public == True).all()


sales_lead_crud = SalesLeadCRUD(SalesLead)
design_package_crud = DesignPackageCRUD(DesignPackage)
case_work_crud = CaseWorkCRUD(CaseWork)
