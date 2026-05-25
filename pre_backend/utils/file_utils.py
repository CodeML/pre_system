"""
文件处理工具
支持上传/下载、格式验证、版本管理
"""

import os
from datetime import datetime
from typing import Tuple, Optional

# 支持的文件类型和格式
SUPPORTED_FILE_TYPES = {
    "设计稿": ["psd", "ai", "fig", "xd", "sketch"],
    "3D模型": ["fbx", "obj", "gltf", "glb", "blend", "max"],
    "摄影图": ["jpg", "jpeg", "png", "tiff", "raw", "psd"],
    "视频": ["mp4", "mov", "avi", "mkv", "webm"],
    "文档": ["pdf", "docx", "xlsx", "pptx"],
    "其他": ["zip", "rar", "txt"]
}

# 文件大小限制（MB）
FILE_SIZE_LIMITS = {
    "设计稿": 1024,      # 1GB
    "3D模型": 2048,     # 2GB
    "摄影图": 512,      # 512MB
    "视频": 5120,       # 5GB
    "文档": 100,        # 100MB
    "其他": 500         # 500MB
}

# 上传目录
UPLOAD_BASE_DIR = "/Users/shaiweiminglei/pre_system/pre_backend/static/uploads"


def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    return filename.rsplit('.', 1)[-1].lower() if '.' in filename else ""


def is_allowed_file_type(file_type: str, file_format: str) -> bool:
    """检查文件格式是否允许"""
    if file_type not in SUPPORTED_FILE_TYPES:
        return False
    return file_format in SUPPORTED_FILE_TYPES[file_type]


def validate_file(filename: str, file_type: str, file_size_mb: float) -> Tuple[bool, str]:
    """
    验证文件
    返回: (valid, error_message)
    """
    # 检查文件类型
    if file_type not in SUPPORTED_FILE_TYPES:
        return False, f"不支持的文件类型: {file_type}。支持的类型: {', '.join(SUPPORTED_FILE_TYPES.keys())}"

    # 检查文件格式
    extension = get_file_extension(filename)
    if not extension:
        return False, "无法识别文件格式（缺少扩展名）"

    if not is_allowed_file_type(file_type, extension):
        allowed = ", ".join(SUPPORTED_FILE_TYPES[file_type])
        return False, f"文件格式不支持。{file_type}支持的格式: {allowed}"

    # 检查文件大小
    max_size = FILE_SIZE_LIMITS.get(file_type, 500)
    if file_size_mb > max_size:
        return False, f"文件过大。{file_type}最大限制: {max_size}MB，实际: {file_size_mb:.2f}MB"

    return True, ""


def generate_version_name(base_name: str, version: int = 1, is_draft: bool = False) -> str:
    """
    生成版本化文件名
    例如: "海报初稿 v1.psd", "海报初稿 v1_draft.psd"
    """
    if '.' in base_name:
        name, ext = base_name.rsplit('.', 1)
    else:
        name = base_name
        ext = ""

    suffix = "_draft" if is_draft else ""
    version_str = f"v{version}{suffix}"

    if ext:
        return f"{name} {version_str}.{ext}"
    else:
        return f"{name} {version_str}"


def generate_upload_path(task_id: int, file_name: str, version: int = 1) -> str:
    """
    生成上传路径
    格式: uploads/task_{task_id}/{year}/{month}/filename_v{version}
    """
    now = datetime.utcnow()
    year = now.year
    month = now.month

    # 确保目录存在
    directory = os.path.join(
        UPLOAD_BASE_DIR,
        f"task_{task_id}",
        str(year),
        f"{month:02d}"
    )

    os.makedirs(directory, exist_ok=True)

    # 生成唯一的文件名
    if '.' in file_name:
        base, ext = file_name.rsplit('.', 1)
        versioned_name = f"{base}_v{version}.{ext}"
    else:
        versioned_name = f"{file_name}_v{version}"

    return os.path.join(directory, versioned_name)


def get_next_version(existing_versions: list) -> int:
    """
    根据现有版本获取下一个版本号
    """
    if not existing_versions:
        return 1

    # 提取版本号并排序
    version_nums = []
    for v in existing_versions:
        try:
            # 假设版本格式为 "v1", "v2" 等
            num = int(v.replace('v', '').split('_')[0])
            version_nums.append(num)
        except ValueError:
            continue

    return max(version_nums) + 1 if version_nums else 1


def compare_file_versions(files: list) -> dict:
    """
    比较多个文件版本
    返回: {latest_version, oldest_version, total_versions, ...}
    """
    if not files:
        return {"error": "没有文件版本可比较"}

    # 提取版本号
    versions = []
    for f in files:
        try:
            num = int(f["version"].replace('v', '').split('_')[0])
            versions.append({
                "version": f["version"],
                "num": num,
                "upload_time": f["upload_time"],
                "size": f.get("size", 0),
                "uploader": f.get("uploader_id")
            })
        except (ValueError, KeyError):
            continue

    if not versions:
        return {"error": "无法解析版本信息"}

    # 排序
    versions.sort(key=lambda x: x["num"], reverse=True)

    return {
        "total_versions": len(versions),
        "latest_version": versions[0] if versions else None,
        "oldest_version": versions[-1] if versions else None,
        "all_versions": versions
    }


def get_file_size_display(size_mb: float) -> str:
    """格式化文件大小显示"""
    if size_mb < 1:
        return f"{size_mb * 1024:.1f} KB"
    elif size_mb < 1024:
        return f"{size_mb:.1f} MB"
    else:
        return f"{size_mb / 1024:.1f} GB"


def get_download_headers(filename: str) -> dict:
    """生成文件下载响应头"""
    return {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/octet-stream"
    }


def calculate_file_hash(file_path: str) -> str:
    """计算文件哈希值（用于去重）"""
    import hashlib
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        return f"error: {str(e)}"


def detect_file_type(filename: str) -> Optional[str]:
    """
    根据文件扩展名推断文件类型
    """
    ext = get_file_extension(filename).lower()

    for file_type, formats in SUPPORTED_FILE_TYPES.items():
        if ext in formats:
            return file_type

    return None


def suggest_file_type(filename: str) -> dict:
    """获取文件类型建议"""
    detected_type = detect_file_type(filename)

    if detected_type:
        return {
            "filename": filename,
            "suggested_type": detected_type,
            "format": get_file_extension(filename),
            "confidence": "high"
        }
    else:
        ext = get_file_extension(filename)
        return {
            "filename": filename,
            "error": f"无法识别的文件格式: .{ext}",
            "available_types": list(SUPPORTED_FILE_TYPES.keys())
        }


def validate_version_name(version_name: str) -> Tuple[bool, str]:
    """验证版本名称格式"""
    # 应该包含 v 和数字
    if 'v' not in version_name:
        return False, "版本名称必须包含版本号（如 v1, v2）"

    try:
        # 尝试提取版本号
        parts = version_name.replace('v', '').split('_')
        int(parts[0])
        return True, ""
    except (ValueError, IndexError):
        return False, f"版本名称格式不正确: {version_name}。应为: v1, v2, v1_draft 等"
