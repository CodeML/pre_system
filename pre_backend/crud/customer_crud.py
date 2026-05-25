from crud.base_crud import BaseCRUD
from models.customer import Customer
from sqlalchemy.orm import Session
from typing import List, Optional


class CustomerCRUD(BaseCRUD):
    def create_customer(self, db: Session, customer_in, creator_id: Optional[int] = None):
        """创建客户（关联创建人）"""
        data = customer_in.dict()
        if creator_id:
            data["creator_id"] = creator_id
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_ecommerce_platform(self, db: Session, platform: str, skip: int = 0, limit: int = 100) -> List[Customer]:
        """按电商平台筛选客户"""
        return db.query(self.model).filter(
            self.model.ecommerce_platform == platform
        ).offset(skip).limit(limit).all()

    def search_by_name(self, db: Session, name: str, skip: int = 0, limit: int = 100) -> List[Customer]:
        """按客户名称模糊搜索"""
        return db.query(self.model).filter(
            self.model.name.contains(name)
        ).offset(skip).limit(limit).all()

    def get_by_creator(self, db: Session, creator_id: int, skip: int = 0, limit: int = 100) -> List[Customer]:
        """获取特定创建人（设计总监）的所有客户"""
        return db.query(self.model).filter(
            self.model.creator_id == creator_id
        ).offset(skip).limit(limit).all()


customer_crud = CustomerCRUD(Customer)
