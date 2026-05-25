from sqlalchemy.orm import Session
from models.base import BaseModel

class BaseCRUD:
    def __init__(self, model):
        self.model = model

    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def get_list(self, db: Session, skip: int = 0, limit: int = 100):
        """获取列表（别名，兼容性）"""
        return self.get_all(db, skip, limit)

    def create(self, db: Session, obj_in):
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, id_or_obj, update_data=None):
        """
        更新对象。支持两种调用方式：
        1. update(db, obj, pydantic_schema) - 原方式
        2. update(db, id, dict_data) - 新方式（ID+字典）
        """
        # 判断第二个参数是否是 ID（int）
        if isinstance(id_or_obj, int):
            # 新方式：ID + 字典更新
            db_obj = self.get(db, id_or_obj)
            if not db_obj:
                return None
            if update_data:
                for key, value in update_data.items():
                    setattr(db_obj, key, value)
        else:
            # 原方式：ORM对象 + Pydantic对象
            db_obj = id_or_obj
            if update_data:
                if hasattr(update_data, 'dict'):
                    # Pydantic 对象
                    update_dict = update_data.dict(exclude_unset=True)
                else:
                    # 字典
                    update_dict = update_data
                for key, value in update_dict.items():
                    setattr(db_obj, key, value)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int):
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        db.delete(db_obj)
        db.commit()
        return db_obj
