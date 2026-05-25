from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from crud.base_crud import BaseCRUD
from models.project import Project


class ProjectCRUD(BaseCRUD):
    """项目 CRUD 操作"""
    
    def create_project(self, db: Session, name: str, customer_id: int, 
                      project_type: str, creator_id: int = None,
                      ecommerce_platform: str = None,
                      main_designer_id: int = None,
                      assist_designer_id: int = None,
                      material_ids: list = None,
                      status: str = "待启动",
                      start_time = None, end_time = None,
                      remark: str = None, **kwargs):
        """创建项目"""
        project = Project(
            name=name,
            customer_id=customer_id,
            type=project_type,
            ecommerce_platform=ecommerce_platform,
            main_designer_id=main_designer_id,
            assist_designer_id=assist_designer_id,
            material_ids=material_ids,
            status=status,
            start_time=start_time,
            end_time=end_time,
            remark=remark,
            **kwargs
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    
    def get_by_customer(self, db: Session, customer_id: int, 
                       skip: int = 0, limit: int = 100) -> List[Project]:
        """按客户查询项目"""
        return db.query(self.model).filter(
            self.model.customer_id == customer_id,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_by_status(self, db: Session, status: str, 
                     skip: int = 0, limit: int = 100) -> List[Project]:
        """按状态查询项目"""
        return db.query(self.model).filter(
            self.model.status == status,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_by_type(self, db: Session, project_type: str,
                   skip: int = 0, limit: int = 100) -> List[Project]:
        """按项目类型查询"""
        return db.query(self.model).filter(
            self.model.type == project_type,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_by_ecommerce_platform(self, db: Session, platform: str,
                                  skip: int = 0, limit: int = 100) -> List[Project]:
        """按电商平台查询"""
        return db.query(self.model).filter(
            self.model.ecommerce_platform == platform,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_by_designer(self, db: Session, designer_id: int,
                       skip: int = 0, limit: int = 100) -> List[Project]:
        """获取设计师相关的项目（主设计师或辅助设计师）"""
        return db.query(self.model).filter(
            or_(
                self.model.main_designer_id == designer_id,
                self.model.assist_designer_id == designer_id
            ),
            self.model.is_active == True
        ).offset(skip).limit(limit).all()
    
    def filter_by_criteria(self, db: Session, customer_id: int = None,
                          status: str = None, project_type: str = None,
                          ecommerce_platform: str = None, designer_id: int = None,
                          skip: int = 0, limit: int = 100) -> List[Project]:
        """多条件筛选项目"""
        query = db.query(self.model).filter(self.model.is_active == True)
        
        if customer_id:
            query = query.filter(self.model.customer_id == customer_id)
        
        if status:
            query = query.filter(self.model.status == status)
        
        if project_type:
            query = query.filter(self.model.type == project_type)
        
        if ecommerce_platform:
            query = query.filter(self.model.ecommerce_platform == ecommerce_platform)
        
        if designer_id:
            query = query.filter(or_(
                self.model.main_designer_id == designer_id,
                self.model.assist_designer_id == designer_id
            ))
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_customer_and_status(self, db: Session, customer_id: int, status: str,
                                   skip: int = 0, limit: int = 100) -> List[Project]:
        """按客户和状态查询项目"""
        return db.query(self.model).filter(
            and_(
                self.model.customer_id == customer_id,
                self.model.status == status,
                self.model.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def update_project_status(self, db: Session, project_id: int, 
                             new_status: str) -> Optional[Project]:
        """更新项目状态"""
        project = self.get(db, project_id)
        if project:
            project.status = new_status
            db.commit()
            db.refresh(project)
        return project
    
    def assign_designers(self, db: Session, project_id: int,
                        main_designer_id: int = None,
                        assist_designer_id: int = None) -> Optional[Project]:
        """分配设计师"""
        project = self.get(db, project_id)
        if project:
            if main_designer_id is not None:
                project.main_designer_id = main_designer_id
            if assist_designer_id is not None:
                project.assist_designer_id = assist_designer_id
            db.commit()
            db.refresh(project)
        return project
    
    def add_material(self, db: Session, project_id: int, material_id: int) -> Optional[Project]:
        """添加素材关联"""
        project = self.get(db, project_id)
        if project:
            if project.material_ids is None:
                project.material_ids = []
            if material_id not in project.material_ids:
                project.material_ids.append(material_id)
            db.commit()
            db.refresh(project)
        return project
    
    def remove_material(self, db: Session, project_id: int, material_id: int) -> Optional[Project]:
        """移除素材关联"""
        project = self.get(db, project_id)
        if project and project.material_ids and material_id in project.material_ids:
            project.material_ids.remove(material_id)
            db.commit()
            db.refresh(project)
        return project

    def clone_project(self, db: Session, source_project_id: int, new_name: str, 
                     creator_id: int = None) -> Optional[Project]:
        """克隆项目（包括任务和素材）"""
        source_project = self.get(db, source_project_id)
        if not source_project:
            return None
        
        # 创建新项目
        new_project = Project(
            name=new_name,
            customer_id=source_project.customer_id,
            type=source_project.type,
            ecommerce_platform=source_project.ecommerce_platform,
            main_designer_id=source_project.main_designer_id,
            assist_designer_id=source_project.assist_designer_id,
            material_ids=source_project.material_ids.copy() if source_project.material_ids else [],
            status="待启动",  # 克隆项目初始状态为待启动
            remark=f"克隆自项目: {source_project.name}"
        )
        db.add(new_project)
        db.flush()  # 获取新项目ID
        
        # 克隆任务
        try:
            from crud.task_crud import task_crud
            source_tasks = db.query(db.model.query(Project).filter(
                Project.id == source_project_id
            )).all()
            
            # 获取源项目的所有任务
            from models.task import Task
            source_tasks = db.query(Task).filter(
                Task.project_id == source_project_id,
                Task.is_active == True
            ).all()
            
            # 复制任务到新项目
            for source_task in source_tasks:
                new_task = Task(
                    project_id=new_project.id,
                    category_id=source_task.category_id,
                    name=source_task.name,
                    designer_id=source_task.designer_id,
                    role_ids=source_task.role_ids.copy() if source_task.role_ids else [],
                    progress=0,
                    status="待开始",
                    ecommerce_params=source_task.ecommerce_params,
                    priority=source_task.priority,
                    description=source_task.description,
                    remark=f"克隆自任务: {source_task.name}"
                )
                db.add(new_task)
        except Exception as e:
            # 任务克隆失败不影响项目克隆
            print(f"项目任务克隆失败: {e}")
        
        db.commit()
        db.refresh(new_project)
        return new_project


# 创建全局实例
project_crud = ProjectCRUD(Project)
