from crud.base_crud import BaseCRUD
from models.after_sales import AfterSalesTicket, RevisionLog
from sqlalchemy.orm import Session


class AfterSalesTicketCRUD(BaseCRUD):
    def get_by_project(self, db: Session, project_id: int):
        return db.query(self.model).filter(self.model.project_id == project_id).all()


class RevisionLogCRUD(BaseCRUD):
    def get_by_task(self, db: Session, task_id: int):
        return db.query(self.model).filter(self.model.task_id == task_id).order_by(self.model.revision_no.desc()).all()

    def add_revision(self, db: Session, task_id: int, description: str, designer_id: int = None, is_paid: str = "false"):
        """添加改稿记录"""
        from models.task import Task
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None
        
        # 增加改稿次数
        task.revision_count += 1
        
        db_obj = self.model(
            task_id=task_id,
            revision_no=task.revision_count,
            description=description,
            designer_id=designer_id,
            is_paid=is_paid
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


after_sales_ticket_crud = AfterSalesTicketCRUD(AfterSalesTicket)
revision_log_crud = RevisionLogCRUD(RevisionLog)
