from crud.base_crud import BaseCRUD
from models.task_category import TaskCategory
from sqlalchemy.orm import Session
from typing import List, Optional
import json


class TaskCategoryCRUD(BaseCRUD):
    def get_subcategories(self, db: Session, parent_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[TaskCategory]:
        """获取子分类（按父分类查询）"""
        query = db.query(self.model).filter(self.model.parent_id == parent_id)
        return query.offset(skip).limit(limit).all()

    def get_all_by_level(self, db: Session, parent_id: Optional[int] = None) -> List[TaskCategory]:
        """获取某一级的所有分类（包括父子关系）"""
        return db.query(self.model).filter(
            self.model.parent_id == parent_id,
            self.model.is_active == True
        ).all()

    def get_tree_structure(self, db: Session, parent_id: Optional[int] = None) -> List[dict]:
        """获取树结构的分类（递归）"""
        categories = self.get_all_by_level(db, parent_id)
        result = []
        
        for cat in categories:
            children = self.get_tree_structure(db, cat.id)
            cat_dict = {
                "id": cat.id,
                "name": cat.name,
                "is_ecommerce": cat.is_ecommerce,
                "description": cat.description,
                "children": children
            }
            result.append(cat_dict)
        
        return result

    def get_by_ecommerce(self, db: Session, skip: int = 0, limit: int = 100) -> List[TaskCategory]:
        """获取电商设计分类"""
        return db.query(self.model).filter(
            self.model.is_ecommerce == True,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_by_roles(self, db: Session, role_ids: List[int], skip: int = 0, limit: int = 100) -> List[TaskCategory]:
        """按用户角色筛选可操作的分类（用户拥有任一角色即可）"""
        categories = db.query(self.model).filter(
            self.model.is_active == True
        ).offset(skip).limit(limit).all()
        
        # 过滤：检查每个分类是否允许用户角色操作
        result = []
        for cat in categories:
            if cat.role_ids is None:
                # 如果分类没有限制，所有人都可以操作
                result.append(cat)
            else:
                # 检查用户角色是否在允许列表中
                allowed_roles = cat.role_ids if isinstance(cat.role_ids, list) else json.loads(cat.role_ids) if isinstance(cat.role_ids, str) else []
                if any(role_id in allowed_roles for role_id in role_ids):
                    result.append(cat)
        
        return result

    def get_parents(self, db: Session, category_id: int) -> List[TaskCategory]:
        """获取分类的所有父分类（祖先链）"""
        result = []
        category = self.get(db, category_id)
        
        while category and category.parent_id:
            parent = self.get(db, category.parent_id)
            if parent:
                result.insert(0, parent)
                category = parent
            else:
                break
        
        return result


task_category_crud = TaskCategoryCRUD(TaskCategory)
