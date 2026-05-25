from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from crud.base_crud import BaseCRUD
from models.file import File
from utils.file_utils import get_next_version


class FileCRUD(BaseCRUD):
    """文件 CRUD 操作"""

    def create_file(self, db: Session, task_id: int, name: str, url: str,
                   file_type: str, uploader_id: int = None, material_id: int = None,
                   file_format: str = None, size: float = None,
                   version: str = "v1", description: str = None, 
                   storage_type: str = "local", storage_key: str = None, **kwargs):
        """创建文件记录"""
        file = File(
            task_id=task_id,
            name=name,
            url=url,
            file_type=file_type,
            uploader_id=uploader_id,
            material_id=material_id,
            file_format=file_format,
            size=size,
            version=version,
            description=description,
            storage_type=storage_type,
            storage_key=storage_key,
            **kwargs
        )
        db.add(file)
        db.commit()
        db.refresh(file)
        return file

    def get_by_task(self, db: Session, task_id: int,
                   skip: int = 0, limit: int = 100) -> List[File]:
        """按任务查询文件"""
        return db.query(self.model).filter(
            self.model.task_id == task_id,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_by_uploader(self, db: Session, uploader_id: int,
                       skip: int = 0, limit: int = 100) -> List[File]:
        """按上传者查询文件"""
        return db.query(self.model).filter(
            self.model.uploader_id == uploader_id,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_by_file_type(self, db: Session, file_type: str,
                        skip: int = 0, limit: int = 100) -> List[File]:
        """按文件类型查询"""
        return db.query(self.model).filter(
            self.model.file_type == file_type,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_by_material(self, db: Session, material_id: int,
                       skip: int = 0, limit: int = 100) -> List[File]:
        """按关联素材查询"""
        return db.query(self.model).filter(
            self.model.material_id == material_id,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_task_versions(self, db: Session, task_id: int, name: str) -> List[File]:
        """获取任务中同一文件的所有版本"""
        return db.query(self.model).filter(
            self.model.task_id == task_id,
            self.model.name == name,
            self.model.is_active == True
        ).order_by(self.model.version.desc()).all()

    def get_latest_version(self, db: Session, task_id: int, name: str) -> Optional[File]:
        """获取最新版本"""
        versions = self.get_task_versions(db, task_id, name)
        return versions[0] if versions else None

    def create_new_version(self, db: Session, task_id: int, name: str, url: str,
                          file_type: str, uploader_id: int = None,
                          file_format: str = None, size: float = None,
                          description: str = None) -> File:
        """创建新版本"""
        # 获取现有版本
        versions = self.get_task_versions(db, task_id, name)
        existing_version_nums = []

        for v in versions:
            try:
                num = int(v.version.replace('v', '').split('_')[0])
                existing_version_nums.append(num)
            except ValueError:
                continue

        # 计算下一个版本号
        next_version_num = max(existing_version_nums) + 1 if existing_version_nums else 1
        new_version = f"v{next_version_num}"

        # 将旧版本标记为非最新
        for v in versions:
            v.is_latest = False
        db.commit()

        # 创建新版本
        new_file = self.create_file(
            db,
            task_id=task_id,
            name=name,
            url=url,
            file_type=file_type,
            uploader_id=uploader_id,
            file_format=file_format,
            size=size,
            version=new_version,
            description=description
        )
        
        # 触发文件版本更新通知
        self._trigger_version_notification(db, new_file)
        
        return new_file

    def confirm_file(self, db: Session, file_id: int, confirm_user_id: int,
                    confirm_remark: str = None) -> Optional[File]:
        """确认文件"""
        file = self.get(db, file_id)
        if file:
            file.is_confirm = True
            file.confirm_user_id = confirm_user_id
            file.confirm_time = datetime.utcnow()
            file.confirm_remark = confirm_remark
            db.commit()
            db.refresh(file)
        return file

    def get_confirmed_files(self, db: Session, task_id: int,
                           skip: int = 0, limit: int = 100) -> List[File]:
        """获取已确认的文件"""
        return db.query(self.model).filter(
            self.model.task_id == task_id,
            self.model.is_confirm == True,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_unconfirmed_files(self, db: Session, task_id: int,
                             skip: int = 0, limit: int = 100) -> List[File]:
        """获取未确认的文件"""
        return db.query(self.model).filter(
            self.model.task_id == task_id,
            self.model.is_confirm == False,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_file_stats(self, db: Session, task_id: int) -> dict:
        """获取任务文件统计"""
        all_files = db.query(self.model).filter(
            self.model.task_id == task_id,
            self.model.is_active == True
        ).all()

        confirmed = len([f for f in all_files if f.is_confirm])
        unconfirmed = len([f for f in all_files if not f.is_confirm])
        total_size = sum(f.size for f in all_files if f.size) or 0

        # 按文件类型统计
        type_stats = {}
        for f in all_files:
            if f.file_type not in type_stats:
                type_stats[f.file_type] = 0
            type_stats[f.file_type] += 1

        return {
            "total_files": len(all_files),
            "confirmed": confirmed,
            "unconfirmed": unconfirmed,
            "total_size_mb": round(total_size, 2),
            "by_type": type_stats
        }

    def _trigger_version_notification(self, db: Session, file: File):
        """触发文件版本更新通知"""
        try:
            from utils.notification_utils import NotificationManager
            from models.task import Task
            
            # 获取任务信息
            if file.task_id:
                task = db.query(Task).filter(Task.id == file.task_id).first()
                if task:
                    # 获取项目负责人
                    from models.project import Project
                    project = db.query(Project).filter(Project.id == task.project_id).first()
                    
                    # 通知项目经理和相关人员
                    if project and project.customer_id:
                        NotificationManager.create_notification(
                            db,
                            sender_id=file.uploader_id,
                            recipient_id=project.creator_id,  # 项目创建人
                            type="file_version_updated",
                            title=f"文件版本更新: {file.name}",
                            content=f"任务 {task.name} 的文件 {file.name} 发布了新版本 {file.version}",
                            priority="high",
                            task_id=file.task_id,
                            project_id=task.project_id
                        )
        except Exception as e:
            # 通知失败不应影响主业务逻辑
            print(f"文件版本通知触发失败: {e}")

    def create_share_link(self, db: Session, file_id: int, expiry_hours: int = 24) -> Optional[File]:
        """创建分享链接"""
        import secrets
        from datetime import timedelta
        
        file = self.get(db, file_id)
        if file:
            file.share_token = secrets.token_urlsafe(32)
            file.share_expiry = datetime.utcnow() + timedelta(hours=expiry_hours)
            file.is_shared = True
            db.commit()
            db.refresh(file)
        return file

    def get_by_share_token(self, db: Session, share_token: str) -> Optional[File]:
        """通过分享令牌获取文件"""
        file = db.query(self.model).filter(
            self.model.share_token == share_token,
            self.model.is_active == True
        ).first()
        
        if file and file.share_expiry:
            if datetime.utcnow() > file.share_expiry:
                # 链接已过期
                return None
        return file

    def revoke_share_link(self, db: Session, file_id: int) -> Optional[File]:
        """撤销分享链接"""
        file = self.get(db, file_id)
        if file:
            file.share_token = None
            file.share_expiry = None
            file.is_shared = False
            db.commit()
            db.refresh(file)
        return file


# 创建全局实例
file_crud = FileCRUD(File)

