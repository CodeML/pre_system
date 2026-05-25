from crud.base_crud import BaseCRUD
from models.user_role import UserRole
from sqlalchemy.orm import Session
from models.role import Role


class UserRoleCRUD(BaseCRUD):
    def assign_role(self, db: Session, user_id: int, role_id: int):
        """为用户分配角色"""
        # 检查是否已分配
        existing = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.role_id == role_id
        ).first()
        if existing:
            return existing
        
        # 创建新关联
        user_role = self.model(user_id=user_id, role_id=role_id)
        db.add(user_role)
        db.commit()
        db.refresh(user_role)
        return user_role

    def revoke_role(self, db: Session, user_id: int, role_id: int):
        """取消用户角色"""
        user_role = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.role_id == role_id
        ).first()
        if user_role:
            db.delete(user_role)
            db.commit()
        return user_role

    def get_user_roles(self, db: Session, user_id: int):
        """获取用户的所有角色对象列表（Role 实例）"""
        # 通过关联表查询 Role 对象，以便上层可以直接读取 role.code
        role_rows = db.query(Role).join(self.model, Role.id == self.model.role_id).filter(self.model.user_id == user_id).all()
        return role_rows


user_role_crud = UserRoleCRUD(UserRole)
