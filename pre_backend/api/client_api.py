from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from database.db import get_db
from models.user import User
from config.auth import get_current_user
from schemas.project_schema import ProjectRead
from schemas.finance_schema import QuotationRead
from schemas.file_schema import FileRead

router = APIRouter()

# ============================================================
# 客户门户 (Client Portal)
# ============================================================

@router.get("/projects", response_model=List[ProjectRead], summary="我的项目", description="客户查看自己名下的所有项目。")
def get_client_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from models.project import Project
    # 实际应用中需根据 current_user 关联的 customer_id 过滤
    return db.query(Project).filter(Project.is_active == True).limit(20).all()


@router.get("/files", response_model=List[FileRead], summary="待确认稿件", description="客户查看所有需要其确认的文件。")
def get_client_pending_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from models.file import File
    return db.query(File).filter(File.is_confirm == False, File.is_active == True).limit(20).all()


@router.get("/quotations", response_model=List[QuotationRead], summary="我的报价单", description="客户查看收到的所有待确认报价单。")
def get_client_quotations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from models.finance import Quotation
    return db.query(Quotation).filter(Quotation.status != 'draft').all()
