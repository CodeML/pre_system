from crud.base_crud import BaseCRUD
from models.task_comment import TaskComment
from sqlalchemy.orm import Session
from typing import List


class TaskCommentCRUD(BaseCRUD):
    def create_comment(self, db: Session, task_id: int, author_id: int, content: str, parent_id: int = None, is_public: bool = True):
        comment = self.model(task_id=task_id, author_id=author_id, content=content, parent_id=parent_id, is_public=is_public)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    def get_comments_by_task(self, db: Session, task_id: int, skip: int = 0, limit: int = 100) -> List[TaskComment]:
        return db.query(self.model).filter(self.model.task_id == task_id, self.model.is_active == True).order_by(self.model.create_time.asc()).offset(skip).limit(limit).all()

    def delete_comment(self, db: Session, comment_id: int, author_id: int = None):
        comment = self.get(db, comment_id)
        if not comment:
            return None
        # 仅作者或管理员可删除：调用方负责权限检查
        comment.is_active = False
        db.commit()
        return comment


task_comment_crud = TaskCommentCRUD(TaskComment)
