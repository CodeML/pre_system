from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File as FastAPIFile, Path, Body
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from config.auth import get_current_user
from database.db import get_db
from models.user import User
from models.file import File
from crud.file_crud import file_crud
from schemas.file_schema import FileCreate, FileRead, FileConfirm, FileUpdate
from utils.file_utils import validate_file
from utils.cloud_storage import get_storage_manager
from config.exceptions import raise_not_found
from config.logger_advanced import get_logger

logger = get_logger()

router = APIRouter()


@router.post("/create", response_model=FileRead, summary="创建文件记录", description="在数据库中手动注册一个文件记录（通常用于关联已有 URL）。")
def create_file(
    file_data: FileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建文件记录"""
    try:
        # 验证文件
        if file_data.size:
            valid, error = validate_file(file_data.name, file_data.file_type, file_data.size)
            if not valid:
                raise HTTPException(status_code=400, detail=error)

        file = file_crud.create_file(
            db,
            task_id=file_data.task_id,
            name=file_data.name,
            url=file_data.url,
            file_type=file_data.file_type,
            uploader_id=current_user.id,
            material_id=file_data.material_id,
            file_format=file_data.file_format,
            size=file_data.size,
            description=file_data.description
        )
        return file
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list", response_model=List[FileRead], summary="获取文件列表", description="分页查询系统内所有活跃文件的记录。")
def list_files(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取文件列表"""
    files = file_crud.get_list(db, skip=skip, limit=limit)
    return files


@router.get("/{file_id}", response_model=FileRead, summary="获取文件详情", description="根据 ID 获取单个文件的详细元数据。")
def get_file(
    file_id: int = Path(..., description="文件ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取文件详情"""
    file = file_crud.get(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")
    return file


@router.put("/{file_id}", response_model=FileRead, summary="更新文件信息", description="修改文件的名称、描述或活跃状态。")
def update_file(
    file_id: int = Path(..., description="文件ID"),
    file_in: FileUpdate = Body(..., description="更新数据"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新文件元数据"""
    file = file_crud.get(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    # 权限检查：只有上传者或管理员可以修改
    from crud.user_role_crud import user_role_crud
    admin_roles = user_role_crud.get_user_roles(db, current_user.id)
    admin_role_names = [role.name for role in admin_roles]
    is_admin = "管理员" in admin_role_names or "超级管理员" in admin_role_names
    
    if file.uploader_id != current_user.id and not is_admin:
        raise HTTPException(status_code=403, detail="无权修改此文件信息")

    updated_file = file_crud.update(db, file_id, file_in)
    return updated_file


@router.get("/filter/by-task/{task_id}", response_model=List[FileRead], summary="按任务筛选文件", description="获取特定任务下上传的所有文件。")
def get_files_by_task(
    task_id: int = Path(..., description="任务ID"),
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按任务查询文件"""
    files = file_crud.get_by_task(db, task_id, skip=skip, limit=limit)
    return files


@router.get("/filter/by-type/{file_type}", response_model=List[FileRead], summary="按类型筛选文件", description="按文件用途类型（如：成品图、素材、参考图）进行筛选。")
def get_files_by_type(
    file_type: str = Path(..., description="文件类型"),
    skip: int = Query(0, ge=0, description="跳过数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按文件类型查询"""
    files = file_crud.get_by_file_type(db, file_type, skip=skip, limit=limit)
    return files


@router.post("/{task_id}/new-version", response_model=FileRead, summary="创建新版本", description="为同一任务下的同名文件上传一个新版本。")
def create_new_version(
    task_id: int = Path(..., description="任务ID"),
    file_data: FileCreate = Body(..., description="文件创建数据"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新版本"""
    try:
        if file_data.size:
            valid, error = validate_file(file_data.name, file_data.file_type, file_data.size)
            if not valid:
                raise HTTPException(status_code=400, detail=error)

        file = file_crud.create_new_version(
            db,
            task_id=task_id,
            name=file_data.name,
            url=file_data.url,
            file_type=file_data.file_type,
            uploader_id=current_user.id,
            file_format=file_data.file_format,
            size=file_data.size,
            description=file_data.description
        )
        return file
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{task_id}/versions", summary="获取版本历史", description="查询特定任务下某个文件的所有历史版本记录。")
def get_file_versions(
    task_id: int = Path(..., description="任务ID"),
    name: str = Query(..., description="文件名称"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取文件版本历史"""
    versions = file_crud.get_task_versions(db, task_id, name)
    return {
        "name": name,
        "total_versions": len(versions),
        "versions": [
            {
                "id": v.id,
                "version": v.version,
                "upload_time": v.upload_time,
                "uploader_id": v.uploader_id,
                "size": v.size,
                "is_latest": v.is_latest
            }
            for v in versions
        ]
    }


@router.put("/{file_id}/confirm", response_model=FileRead, summary="确认文件", description="标记文件为已通过客户确认，并可附带备注信息。")
def confirm_file(
    file_id: int = Path(..., description="文件ID"),
    confirm_data: FileConfirm = Body(..., description="确认数据"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """确认文件"""
    file = file_crud.confirm_file(
        db, file_id, current_user.id,
        confirm_remark=confirm_data.confirm_remark
    )
    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")
    return file


@router.get("/{task_id}/stats", summary="获取文件统计", description="统计特定任务下的文件总数、确认数等信息。")
def get_file_stats(
    task_id: int = Path(..., description="任务ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务文件统计"""
    stats = file_crud.get_file_stats(db, task_id)
    return stats


@router.delete("/{file_id}", summary="删除文件", description="软删除指定文件记录。")
def delete_file(
    file_id: int = Path(..., description="文件ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除文件"""
    file = file_crud.get(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    file_crud.update(db, file_id, {'is_active': False})
    return {"message": "文件已删除"}


@router.post("/upload", summary="上传文件", description="将文件上传至本地或 S3 云存储，并自动创建数据库记录。支持设置任务或素材关联。")
async def upload_file(
    file: UploadFile = FastAPIFile(..., description="要上传的文件对象"),
    task_id: Optional[int] = Query(None, description="关联任务ID"),
    material_id: Optional[int] = Query(None, description="关联素材ID"),
    storage_type: str = Query("local", description="存储类型 (local/s3)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    上传文件到云存储
    
    支持多种存储类型 (local/s3)
    """
    try:
        # 验证文件大小和类型
        content = await file.read()
        file_size = len(content)
        
        valid, error = validate_file(file.filename, file.content_type, file_size)
        if not valid:
            raise HTTPException(status_code=400, detail=error)
        
        # 使用云存储管理器上传
        storage_manager = get_storage_manager()
        
        # 创建类文件对象用于上传
        from io import BytesIO
        file_obj = BytesIO(content)
        
        upload_result = storage_manager.upload(
            file_path=file.filename,
            file_content=file_obj,
            adapter_name=storage_type,
            metadata={
                "original_name": file.filename,
                "uploader_id": current_user.id
            }
        )
        
        # 保存文件记录到数据库
        db_file = file_crud.create_file(
            db,
            task_id=task_id,
            name=file.filename,
            url=upload_result["url"],
            file_type=upload_result["content_type"],
            uploader_id=current_user.id,
            material_id=material_id,
            file_format=file.filename.split(".")[-1] if "." in file.filename else "unknown",
            size=file_size,
            storage_key=upload_result.get("key", ""),
            storage_type=storage_type
        )
        
        logger.info(f"File uploaded successfully: {file.filename} by user {current_user.id}")
        
        return {
            "id": db_file.id,
            "name": db_file.name,
            "url": db_file.url,
            "size": db_file.size,
            "storage_type": storage_type,
            "uploaded_at": db_file.upload_time.isoformat() if db_file.upload_time else None,
            "download_url": f"/api/file/{db_file.id}/download"
        }
        
    except Exception as e:
        logger.error(f"File upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")


@router.get("/{file_id}/download", summary="下载文件", description="根据文件记录 ID 获取文件流，支持各种存储后端。")
def download_file(
    file_id: int = Path(..., description="文件ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    下载文件
    
    支持多种存储类型，自动识别并调用相应的下载方法
    """
    try:
        file = file_crud.get(db, file_id)
        if not file:
            raise_not_found("文件", file_id)
        
        storage_type = getattr(file, 'storage_type', 'local') or 'local'
        storage_manager = get_storage_manager()
        
        # 如果存储了 storage_key，使用它；否则用 url 作为 key
        file_key = getattr(file, 'storage_key', None) or file.url
        
        logger.info(f"Downloading file: {file.name} (key={file_key}, type={storage_type})")
        
        # 获取文件流
        file_stream = storage_manager.download(file_key, adapter_name=storage_type)
        
        # 返回流式响应
        return StreamingResponse(
            file_stream,
            media_type=file.file_type or "application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename={file.name}"
            }
        )
        
    except FileNotFoundError as e:
        raise_not_found("文件", str(e))
    except Exception as e:
        logger.error(f"File download failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文件下载失败: {str(e)}")


@router.get("/{file_id}/info", summary="获取文件详情及下载链接", description="返回文件的详细元数据，并生成直接下载的临时或永久链接。")
def get_file_info(
    file_id: int = Path(..., description="文件ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取文件详细信息及下载 URL"""
    try:
        file = file_crud.get(db, file_id)
        if not file:
            raise_not_found("文件", file_id)
        
        storage_type = getattr(file, 'storage_type', 'local') or 'local'
        storage_manager = get_storage_manager()
        
        file_key = getattr(file, 'storage_key', None) or file.url
        
        # 获取文件信息
        info = storage_manager.get_file_info(file_key, adapter_name=storage_type)
        
        # 获取下载 URL（可选：S3 预签名 URL，默认 URL）
        download_url = storage_manager.get_download_url(file_key, adapter_name=storage_type)
        
        return {
            **info,
            "id": file.id,
            "name": file.name,
            "download_url": download_url,
            "direct_api_url": f"/api/file/{file_id}/download"
        }
        
    except Exception as e:
        logger.error(f"Get file info failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取文件信息失败: {str(e)}")


# ============================================================
# 文件分享
# ============================================================

@router.post("/{file_id}/share", summary="创建分享链接", description="为指定文件生成一个带有有效期的临时分享令牌。")
def create_share_link(
    file_id: int = Path(..., description="文件ID"),
    expiry_hours: int = Query(24, ge=1, le=720, description="有效期（小时）"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建文件分享链接"""
    try:
        file = file_crud.get(db, file_id)
        if not file:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        file = file_crud.create_share_link(db, file_id, expiry_hours=expiry_hours)
        return {
            "file_id": file.id,
            "share_token": file.share_token,
            "share_url": f"/api/file/share/{file.share_token}",
            "expiry": file.share_expiry.isoformat() if file.share_expiry else None,
            "message": f"分享链接有效期: {expiry_hours} 小时"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/share/{share_token}", summary="访问分享文件", description="通过分享令牌获取文件的基本信息及下载地址。")
def access_shared_file(
    share_token: str = Path(..., description="分享令牌"),
    db: Session = Depends(get_db)
):
    """通过分享令牌访问文件"""
    try:
        file = file_crud.get_by_share_token(db, share_token)
        if not file:
            raise HTTPException(status_code=404, detail="分享链接不存在或已过期")
        
        return {
            "id": file.id,
            "name": file.name,
            "description": file.description,
            "file_type": file.file_type,
            "size": file.size,
            "upload_time": file.upload_time,
            "download_url": f"/api/file/{file.id}/download"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{file_id}/share", summary="撤销分享链接", description="立即使文件的分享链接失效。")
def revoke_share_link(
    file_id: int = Path(..., description="文件ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """撤销文件分享链接"""
    try:
        file = file_crud.get(db, file_id)
        if not file:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        file = file_crud.revoke_share_link(db, file_id)
        return {"message": "分享链接已撤销"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

