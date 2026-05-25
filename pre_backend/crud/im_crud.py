from crud.base_crud import BaseCRUD
from models.im import ChatSession, ChatSessionMember, ChatMessage
from sqlalchemy.orm import Session
from datetime import datetime


class ChatSessionCRUD(BaseCRUD):
    def create_with_members(self, db: Session, session_in, creator_id: int):
        # 创建会话
        db_obj = self.model(
            name=session_in.name,
            type=session_in.type,
            project_id=session_in.project_id
        )
        db.add(db_obj)
        db.flush()
        
        # 添加成员
        member_ids = set(session_in.member_ids)
        member_ids.add(creator_id)
        
        for uid in member_ids:
            member = ChatSessionMember(
                session_id=db_obj.id,
                user_id=uid,
                is_admin=(uid == creator_id)
            )
            db.add(member)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_user_sessions(self, db: Session, user_id: int):
        return db.query(self.model).join(ChatSessionMember).filter(ChatSessionMember.user_id == user_id).all()


class ChatMessageCRUD(BaseCRUD):
    def get_session_messages(self, db: Session, session_id: int, skip: int = 0, limit: int = 50):
        return db.query(self.model).filter(self.model.session_id == session_id).order_by(self.model.create_time.desc()).offset(skip).limit(limit).all()

    def send_message(self, db: Session, msg_in, sender_id: int):
        db_obj = self.model(
            **msg_in.model_dump(),
            sender_id=sender_id
        )
        db.add(db_obj)
        
        # 更新会话最后活跃时间
        session = db.query(ChatSession).filter(ChatSession.id == msg_in.session_id).first()
        if session:
            session.last_message_at = datetime.utcnow()
        
        db.commit()
        db.refresh(db_obj)
        return db_obj


chat_session_crud = ChatSessionCRUD(ChatSession)
chat_message_crud = ChatMessageCRUD(ChatMessage)
