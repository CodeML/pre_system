from crud.base_crud import BaseCRUD
from models.user import User
from models.role import Role
from config.auth import get_password_hash, verify_password
from sqlalchemy.orm import Session


class UserCRUD(BaseCRUD):
	def create_user(self, db, user_in):
		"""创建用户（哈希密码）"""
		# user_in expected to be a Pydantic model with .dict()
		data = user_in.dict()
		password = data.pop("password", None)
		if password:
			data["password"] = get_password_hash(password)
		db_obj = self.model(**data)
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)
		return db_obj

	def authenticate_user(self, db, username: str, password: str):
		"""认证用户（验证密码）"""
		user = db.query(self.model).filter(self.model.username == username).first()
		if not user:
			return None
		if not verify_password(password, user.password):
			return None
		return user

	def get_user_with_roles(self, db: Session, user_id: int):
		"""获取用户及其关联的角色列表"""
		user = db.query(self.model).filter(self.model.id == user_id).first()
		if not user:
			return None
		# 从关联表获取角色ID列表
		from models.user_role import UserRole
		role_ids = db.query(UserRole.role_id).filter(UserRole.user_id == user_id).all()
		roles = db.query(Role).filter(Role.id.in_([rid[0] for rid in role_ids])).all()
		return {"user": user, "roles": roles}

	def reset_password(self, db: Session, user_id: int, new_password: str):
		"""重置用户密码"""
		user = self.get(db, user_id)
		if user:
			user.password = get_password_hash(new_password)
			db.commit()
			db.refresh(user)
		return user

	def reset_password_by_username(self, db: Session, username: str, new_password: str):
		"""通过用户名重置密码"""
		user = db.query(self.model).filter(self.model.username == username).first()
		if user:
			user.password = get_password_hash(new_password)
			db.commit()
			db.refresh(user)
		return user


user_crud = UserCRUD(User)