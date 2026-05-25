from crud.base_crud import BaseCRUD
from models.permission import Permission
from sqlalchemy.orm import Session


class PermissionCRUD(BaseCRUD):
    def create_if_not_exists(self, db: Session, code: str, name: str = None, description: str = None):
        perm = db.query(self.model).filter(self.model.code == code).first()
        if perm:
            return perm
        perm = self.model(code=code, name=name, description=description)
        db.add(perm)
        db.commit()
        db.refresh(perm)
        return perm

    def assign_to_role(self, db: Session, permission_id: int, role):
        """将权限分配给 Role 实例（role 为 Role 对象）"""
        perm = db.query(self.model).get(permission_id)
        if not perm:
            return None
        if perm not in role.permissions:
            role.permissions.append(perm)
            db.add(role)
            db.commit()
        return perm

    def revoke_from_role(self, db: Session, permission_id: int, role):
        perm = db.query(self.model).get(permission_id)
        if not perm:
            return None
        if perm in role.permissions:
            role.permissions.remove(perm)
            db.add(role)
            db.commit()
        return perm


permission_crud = PermissionCRUD(Permission)
