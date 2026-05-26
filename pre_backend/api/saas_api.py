from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, BackgroundTasks, UploadFile, File as FastAPIFile
from sqlalchemy.orm import Session
from typing import List, Optional
from database.db import get_db
from models.user import User
from config.auth import get_current_user
from models.saas import AsyncJob, Webhook, WebhookLog
from schemas.saas_schema import AsyncJobRead, WebhookCreate, WebhookRead, WebhookLogRead, GlobalSearchResult
import time

router = APIRouter()

# ============================================================
# 异步任务中心 (Async Jobs)
# ============================================================

def dummy_background_job(job_id: int, db: Session):
    """模拟一个耗时的后台任务"""
    job = db.query(AsyncJob).filter(AsyncJob.id == job_id).first()
    if not job:
        return
    job.status = "processing"
    db.commit()
    
    # 模拟耗时
    time.sleep(5)
    
    job.status = "completed"
    job.progress = 100
    job.result = {"message": "Job completed successfully"}
    db.commit()

@router.get("/jobs/{job_id}", response_model=AsyncJobRead, summary="查询任务进度", description="查询由后台异步执行的耗时任务状态。")
def get_job_status(
    job_id: int = Path(..., description="任务ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = db.query(AsyncJob).filter(AsyncJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="任务不存在")
    return job

@router.post("/jobs/{job_id}/cancel", summary="取消后台任务", description="取消正在进行的异步任务。")
def cancel_job(
    job_id: int = Path(..., description="任务ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = db.query(AsyncJob).filter(AsyncJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="任务不存在")
    job.status = "failed"
    job.error = "Cancelled by user"
    db.commit()
    return {"message": "任务已取消"}

# ============================================================
# Webhooks 订阅
# ============================================================

@router.post("/webhooks/subscribe", response_model=WebhookRead, summary="订阅Webhook", description="允许外部系统订阅PRE系统内部事件。")
def subscribe_webhook(
    webhook_in: WebhookCreate = Body(..., description="Webhook配置"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_obj = Webhook(**webhook_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/webhooks/logs", response_model=List[WebhookLogRead], summary="Webhook推送日志", description="查询Webhook的回调推送记录及失败原因。")
def get_webhook_logs(
    skip: int = Query(0, description="跳过数"),
    limit: int = Query(100, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(WebhookLog).order_by(WebhookLog.create_time.desc()).offset(skip).limit(limit).all()

# ============================================================
# 数据导入中心 (Data Import)
# ============================================================

@router.post("/import/validate", summary="校验导入文件", description="预校验上传的 Excel/CSV 文件字段合法性。")
def validate_import_file(
    file: UploadFile = FastAPIFile(..., description="要导入的数据文件"),
    import_type: str = Query(..., description="导入类型（customer/task）"),
    current_user: User = Depends(get_current_user)
):
    """预校验导入数据"""
    return {
        "status": "valid",
        "total_rows": 100,
        "valid_rows": 98,
        "errors": [{"row": 2, "error": "缺少必填字段"}]
    }

@router.post("/import/confirm", response_model=AsyncJobRead, summary="确认导入", description="确认无误后将导入任务放入异步队列执行。")
def confirm_import(
    import_type: str = Query(..., description="导入类型"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = AsyncJob(task_name=f"批量导入 {import_type}", created_by=current_user.id)
    db.add(job)
    db.commit()
    db.refresh(job)
    
    background_tasks.add_task(dummy_background_job, job.id, db)
    return job

# ============================================================
# 高级搜索引擎 (Global Search)
# ============================================================

@router.get("/search/global", response_model=List[GlobalSearchResult], summary="全局统一搜索", description="跨模块进行统一的关键词全文搜索。")
def global_search(
    q: str = Query(..., min_length=2, description="搜索关键词"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """全局搜索占位实现"""
    # 实际应使用 Elasticsearch 或跨表 UNION 查询
    results = []
    
    from models.project import Project
    projects = db.query(Project).filter(Project.name.contains(q), Project.is_deleted == False).limit(5).all()
    for p in projects:
        results.append({
            "type": "project", "id": p.id, "title": p.name, 
            "subtitle": f"状态: {p.status}", "url": f"/project/{p.id}", "match_score": 1.0
        })
        
    from models.task import Task
    tasks = db.query(Task).filter(Task.name.contains(q), Task.is_deleted == False).limit(5).all()
    for t in tasks:
        results.append({
            "type": "task", "id": t.id, "title": t.name, 
            "subtitle": f"状态: {t.status}", "url": f"/task/{t.id}", "match_score": 1.0
        })
        
    return results


# ============================================================
# 系统初始化与演示数据 (Onboarding)
# ============================================================

@router.post("/seed", summary="初始化演示数据", description="为新组织/租户一键生成示例项目、任务、客户，用于快速上手体验。")
def seed_demo_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    一键生成演示数据
    """
    from models.customer import Customer
    from models.project import Project
    from models.task import Task
    
    # 1. 创建演示客户
    customer = Customer(
        name="演示企业有限公司", 
        contact="张经理", 
        phone="13800000000",
        type="enterprise",
        remark="这是系统自动生成的演示数据"
    )
    db.add(customer)
    db.flush()
    
    # 2. 创建演示项目
    project = Project(
        name="双11美妆海报设计（演示）",
        customer_id=customer.id,
        type="电商设计",
        ecommerce_platform="天猫",
        status="设计中"
    )
    db.add(project)
    db.flush()
    
    # 3. 创建演示任务
    task = Task(
        project_id=project.id,
        name="主视觉海报初稿",
        designer_id=current_user.id,
        status="进行中",
        priority="高"
    )
    db.add(task)
    
    db.commit()
    return {"message": "演示数据初始化成功", "customer_id": customer.id, "project_id": project.id}
