from sqlalchemy.orm import Session
from models.base import BaseModel
from datetime import datetime

class BaseCRUD:
    def __init__(self, model):
        self.model = model

    def get(self, db: Session, id: int):
        """获取单个对象（排除已逻辑删除的）"""
        return db.query(self.model).filter(
            self.model.id == id,
            self.model.is_deleted == False
        ).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        """获取所有对象（排除已逻辑删除的）"""
        return db.query(self.model).filter(
            self.model.is_deleted == False
        ).offset(skip).limit(limit).all()
    
    def get_list(self, db: Session, skip: int = 0, limit: int = 100):
        """获取列表（别名，兼容性）"""
        return self.get_all(db, skip, limit)

    def create(self, db: Session, obj_in, commit=True):
        """创建对象，支持延迟提交（用于事务）"""
        if hasattr(obj_in, 'model_dump'):
            obj_data = obj_in.model_dump()
        elif hasattr(obj_in, 'dict'):
            obj_data = obj_in.dict()
        else:
            obj_data = obj_in
            
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        if commit:
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, id_or_obj, update_data=None, commit=True):
        """
        更新对象，支持延迟提交（用于事务）
        """
        if isinstance(id_or_obj, int):
            db_obj = self.get(db, id_or_obj)
            if not db_obj:
                return None
            update_dict = update_data
        else:
            db_obj = id_or_obj
            if hasattr(update_data, 'model_dump'):
                update_dict = update_data.model_dump(exclude_unset=True)
            elif hasattr(update_data, 'dict'):
                update_dict = update_data.dict(exclude_unset=True)
            else:
                update_dict = update_data

        if update_dict:
            for key, value in update_dict.items():
                setattr(db_obj, key, value)
        
        if commit:
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int, commit=True):
        """逻辑删除"""
        db_obj = self.get(db, id)
        if db_obj:
            db_obj.is_deleted = True
            db_obj.delete_time = datetime.utcnow()
            if commit:
                db.commit()
        return db_obj

    def hard_delete(self, db: Session, id: int, commit=True):
        """物理删除（极少使用）"""
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if db_obj:
            db.delete(db_obj)
            if commit:
                db.commit()
        return db_obj
