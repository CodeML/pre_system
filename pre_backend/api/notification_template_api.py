from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from database.db import get_db
from models.user import User
from models.notification import NotificationTemplate
from config.auth import get_current_user
from pydantic import BaseModel, Field
from typing import List, Optional

router = APIRouter()

class TemplateCreate(BaseModel):
    code: str
    title_tpl: str
    content_tpl: str
    type: Optional[str] = "system"

@router.post("/templates", summary="创建通知模版")
def create_template(
    t_in: TemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_obj = NotificationTemplate(**t_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/templates/list", summary="获取模版列表")
def list_templates(db: Session = Depends(get_db)):
    return db.query(NotificationTemplate).filter(NotificationTemplate.is_active == True).all()

@router.put("/templates/{code}", summary="更新模版内容")
def update_template(
    code: str = Path(...),
    t_in: TemplateCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tpl = db.query(NotificationTemplate).filter(NotificationTemplate.code == code).first()
    if not tpl:
        raise HTTPException(status_code=404, detail="模版不存在")
    tpl.title_tpl = t_in.title_tpl
    tpl.content_tpl = t_in.content_tpl
    db.commit()
    return tpl
