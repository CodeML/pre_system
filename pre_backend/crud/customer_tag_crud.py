"""
客户标签 CRUD 操作层
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models.customer_tag import CustomerTag, CustomerTagAssociation
from crud.base_crud import BaseCRUD


class CustomerTagCRUD(BaseCRUD):
    """客户标签 CRUD 操作"""

    def search_by_name(self, db: Session, name: str, 
                      is_active: bool = True) -> List[CustomerTag]:
        """按名称搜索标签"""
        query = db.query(CustomerTag).filter(
            CustomerTag.name.contains(name)
        )
        if is_active:
            query = query.filter(CustomerTag.is_active == True)
        return query.all()

    def get_by_category(self, db: Session, category: str,
                       is_active: bool = True) -> List[CustomerTag]:
        """按类别获取标签"""
        query = db.query(CustomerTag).filter(
            CustomerTag.category == category
        )
        if is_active:
            query = query.filter(CustomerTag.is_active == True)
        return query.all()

    def get_popular_tags(self, db: Session, limit: int = 10,
                        is_active: bool = True) -> List[CustomerTag]:
        """获取热门标签（按使用次数排序）"""
        query = db.query(CustomerTag)
        if is_active:
            query = query.filter(CustomerTag.is_active == True)
        return query.order_by(CustomerTag.usage_count.desc()).limit(limit).all()

    def assign_tag_to_customer(self, db: Session, customer_id: int, 
                              tag_id: int, assigned_by: int,
                              remark: str = None) -> CustomerTagAssociation:
        """为客户分配标签"""
        # 检查是否已存在关联
        existing = db.query(CustomerTagAssociation).filter(
            and_(
                CustomerTagAssociation.customer_id == customer_id,
                CustomerTagAssociation.tag_id == tag_id
            )
        ).first()
        
        if existing:
            return existing
        
        # 创建新关联
        association = CustomerTagAssociation(
            customer_id=customer_id,
            tag_id=tag_id,
            assigned_by=assigned_by,
            remark=remark
        )
        db.add(association)
        
        # 增加标签使用计数
        tag = self.get(db, tag_id)
        if tag:
            tag.usage_count += 1
        
        db.commit()
        db.refresh(association)
        return association

    def remove_tag_from_customer(self, db: Session, customer_id: int, 
                                tag_id: int) -> bool:
        """移除客户的标签"""
        association = db.query(CustomerTagAssociation).filter(
            and_(
                CustomerTagAssociation.customer_id == customer_id,
                CustomerTagAssociation.tag_id == tag_id
            )
        ).first()
        
        if not association:
            return False
        
        db.delete(association)
        
        # 减少标签使用计数
        tag = self.get(db, tag_id)
        if tag and tag.usage_count > 0:
            tag.usage_count -= 1
        
        db.commit()
        return True

    def get_customer_tags(self, db: Session, customer_id: int) -> List[CustomerTag]:
        """获取客户的所有标签"""
        associations = db.query(CustomerTagAssociation).filter(
            CustomerTagAssociation.customer_id == customer_id
        ).all()
        
        tags = []
        for assoc in associations:
            tag = self.get(db, assoc.tag_id)
            if tag:
                tags.append(tag)
        return tags

    def get_customers_by_tag(self, db: Session, tag_id: int) -> List[int]:
        """获取具有某标签的所有客户ID"""
        associations = db.query(CustomerTagAssociation).filter(
            CustomerTagAssociation.tag_id == tag_id
        ).all()
        return [assoc.customer_id for assoc in associations]

    def bulk_assign_tags(self, db: Session, customer_id: int, 
                        tag_ids: List[int], assigned_by: int) -> int:
        """批量分配标签给客户"""
        count = 0
        for tag_id in tag_ids:
            try:
                self.assign_tag_to_customer(db, customer_id, tag_id, assigned_by)
                count += 1
            except Exception:
                continue
        return count

    def create_predefined_tags(self, db: Session) -> int:
        """创建预定义的标签"""
        predefined_tags = [
            # 设计服务类
            {"name": "详情页设计", "category": "service", "color": "#FF6B6B"},
            {"name": "3D建模", "category": "service", "color": "#4ECDC4"},
            {"name": "摄影处理", "category": "service", "color": "#45B7D1"},
            {"name": "视频制作", "category": "service", "color": "#96CEB4"},
            
            # 电商平台类
            {"name": "淘宝", "category": "platform", "color": "#FF8C00"},
            {"name": "抖音", "category": "platform", "color": "#000000"},
            {"name": "小红书", "category": "platform", "color": "#FF1744"},
            {"name": "Amazon", "category": "platform", "color": "#FF9900"},
            
            # 客户规模类
            {"name": "个人客户", "category": "skill", "color": "#B19CD9"},
            {"name": "中小企业", "category": "skill", "color": "#7FD8BE"},
            {"name": "大型企业", "category": "skill", "color": "#FFB6B9"},
        ]
        
        count = 0
        for tag_data in predefined_tags:
            # 检查是否已存在
            existing = db.query(CustomerTag).filter(
                CustomerTag.name == tag_data["name"]
            ).first()
            
            if not existing:
                tag = CustomerTag(
                    name=tag_data["name"],
                    category=tag_data.get("category"),
                    color=tag_data.get("color"),
                    description=f"{tag_data['name']} 标签"
                )
                db.add(tag)
                count += 1
        
        db.commit()
        return count


# 创建全局实例
customer_tag_crud = CustomerTagCRUD(CustomerTag)
