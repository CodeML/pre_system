from sqlalchemy.orm import Session
from typing import List, Optional
from crud.base_crud import BaseCRUD
from models.material import Material


class MaterialCRUD(BaseCRUD):
    """素材库 CRUD 操作"""

    def create_material(self, db: Session, name: str, type: str, url: str,
                       uploader_id: int = None, category: str = None,
                       file_format: str = None, size: int = None,
                       project_ids: list = None, is_reusable: bool = True,
                       tags: list = None, description: str = None, **kwargs):
        """创建素材"""
        material = Material(
            name=name,
            type=type,
            url=url,
            uploader_id=uploader_id,
            category=category,
            file_format=file_format,
            size=size,
            project_ids=project_ids or [],
            is_reusable=is_reusable,
            tags=tags or [],
            description=description,
            **kwargs
        )
        db.add(material)
        db.commit()
        db.refresh(material)
        return material

    def get_by_type(self, db: Session, material_type: str,
                   skip: int = 0, limit: int = 100) -> List[Material]:
        """按类型查询素材"""
        return db.query(self.model).filter(
            self.model.type == material_type,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_by_category(self, db: Session, category: str,
                       skip: int = 0, limit: int = 100) -> List[Material]:
        """按分类查询素材"""
        return db.query(self.model).filter(
            self.model.category == category,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_reusable(self, db: Session, skip: int = 0, limit: int = 100) -> List[Material]:
        """获取可复用素材"""
        return db.query(self.model).filter(
            self.model.is_reusable == True,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_by_uploader(self, db: Session, uploader_id: int,
                       skip: int = 0, limit: int = 100) -> List[Material]:
        """按上传者查询素材"""
        return db.query(self.model).filter(
            self.model.uploader_id == uploader_id,
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_by_project(self, db: Session, project_id: int,
                      skip: int = 0, limit: int = 100) -> List[Material]:
        """获取项目相关的素材"""
        all_materials = db.query(self.model).filter(
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

        # 过滤包含该项目 ID 的素材
        return [
            m for m in all_materials
            if m.project_ids and project_id in m.project_ids
        ]

    def search_by_name(self, db: Session, keyword: str,
                      skip: int = 0, limit: int = 100) -> List[Material]:
        """按名称搜索素材"""
        return db.query(self.model).filter(
            self.model.name.contains(keyword),
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def add_project(self, db: Session, material_id: int, project_id: int) -> Optional[Material]:
        """添加项目关联"""
        from sqlalchemy.orm import attributes
        material = self.get(db, material_id)
        if material:
            if material.project_ids is None:
                material.project_ids = []
            if project_id not in material.project_ids:
                material.project_ids.append(project_id)
                # 标记 JSON 列已修改
                attributes.flag_modified(material, "project_ids")
            db.commit()
            db.refresh(material)
        return material

    def remove_project(self, db: Session, material_id: int, project_id: int) -> Optional[Material]:
        """移除项目关联"""
        from sqlalchemy.orm import attributes
        material = self.get(db, material_id)
        if material and material.project_ids and project_id in material.project_ids:
            material.project_ids.remove(project_id)
            attributes.flag_modified(material, "project_ids")
            db.commit()
            db.refresh(material)
        return material

    def add_task(self, db: Session, material_id: int, task_id: int) -> Optional[Material]:
        """添加任务关联"""
        from sqlalchemy.orm import attributes
        material = self.get(db, material_id)
        if material:
            if material.task_ids is None:
                material.task_ids = []
            if task_id not in material.task_ids:
                material.task_ids.append(task_id)
                attributes.flag_modified(material, "task_ids")
            db.commit()
            db.refresh(material)
        return material

    def remove_task(self, db: Session, material_id: int, task_id: int) -> Optional[Material]:
        """移除任务关联"""
        from sqlalchemy.orm import attributes
        material = self.get(db, material_id)
        if material and material.task_ids and task_id in material.task_ids:
            material.task_ids.remove(task_id)
            attributes.flag_modified(material, "task_ids")
            db.commit()
            db.refresh(material)
        return material

    def get_by_task(self, db: Session, task_id: int,
                   skip: int = 0, limit: int = 100) -> List[Material]:
        """获取任务相关的素材"""
        all_materials = db.query(self.model).filter(
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

        # 过滤包含该任务 ID 的素材
        return [
            m for m in all_materials
            if m.task_ids and task_id in m.task_ids
        ]

    def add_tag(self, db: Session, material_id: int, tag: str) -> Optional[Material]:
        """添加标签"""
        from sqlalchemy.orm import attributes
        material = self.get(db, material_id)
        if material:
            if material.tags is None:
                material.tags = []
            if tag not in material.tags:
                material.tags.append(tag)
                attributes.flag_modified(material, "tags")
            db.commit()
            db.refresh(material)
        return material

    def remove_tag(self, db: Session, material_id: int, tag: str) -> Optional[Material]:
        """移除标签"""
        from sqlalchemy.orm import attributes
        material = self.get(db, material_id)
        if material and material.tags and tag in material.tags:
            material.tags.remove(tag)
            attributes.flag_modified(material, "tags")
            db.commit()
            db.refresh(material)
        return material

    def increment_reuse_count(self, db: Session, material_id: int) -> Optional[Material]:
        """增加复用次数"""
        material = self.get(db, material_id)
        if material:
            material.reuse_count = (material.reuse_count or 0) + 1
            db.commit()
            db.refresh(material)
        return material

    def get_by_tag(self, db: Session, tag: str,
                  skip: int = 0, limit: int = 100) -> List[Material]:
        """按标签查询素材"""
        all_materials = db.query(self.model).filter(
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

        # 过滤包含该标签的素材
        return [
            m for m in all_materials
            if m.tags and tag in m.tags
        ]

    def get_popular_materials(self, db: Session, limit: int = 10) -> List[Material]:
        """获取热门素材（复用次数最多）"""
        return db.query(self.model).filter(
            self.model.is_active == True,
            self.model.is_reusable == True
        ).order_by(self.model.reuse_count.desc()).limit(limit).all()

    def get_material_stats(self, db: Session) -> dict:
        """获取素材库统计"""
        all_materials = db.query(self.model).filter(
            self.model.is_active == True
        ).all()

        reusable = len([m for m in all_materials if m.is_reusable])
        total_reuse = sum(m.reuse_count for m in all_materials if m.reuse_count)

        # 按类型统计
        type_stats = {}
        for m in all_materials:
            if m.type not in type_stats:
                type_stats[m.type] = 0
            type_stats[m.type] += 1

        return {
            "total_materials": len(all_materials),
            "reusable_materials": reusable,
            "total_reuse_count": total_reuse,
            "average_reuse": round(total_reuse / len(all_materials), 2) if all_materials else 0,
            "by_type": type_stats
        }


# 创建全局实例
material_crud = MaterialCRUD(Material)
