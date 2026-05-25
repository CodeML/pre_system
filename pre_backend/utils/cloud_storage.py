"""
云存储管理模块 - 支持 S3/阿里云OSS/本地存储
支持多适配器架构，生产环境可快速切换
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, BinaryIO
from datetime import datetime
import mimetypes
import os
from config.logger_advanced import get_logger

logger = get_logger()


class CloudStorageAdapter(ABC):
    """云存储适配器基类"""
    
    @abstractmethod
    def upload(self, file_path: str, file_content: BinaryIO, metadata: dict = None) -> dict:
        """上传文件，返回 {url, key, size, content_type}"""
        pass
    
    @abstractmethod
    def download(self, file_key: str) -> BinaryIO:
        """下载文件"""
        pass
    
    @abstractmethod
    def delete(self, file_key: str) -> bool:
        """删除文件"""
        pass
    
    @abstractmethod
    def get_download_url(self, file_key: str, expires_in: int = 3600) -> str:
        """获取下载 URL"""
        pass
    
    @abstractmethod
    def list_files(self, prefix: str = "", max_keys: int = 100) -> list:
        """列出文件"""
        pass
    
    @abstractmethod
    def get_file_info(self, file_key: str) -> dict:
        """获取文件信息"""
        pass


class LocalStorageAdapter(CloudStorageAdapter):
    """本地存储适配器"""
    
    def __init__(self, base_path: str = "static/uploads"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"LocalStorageAdapter initialized: {self.base_path}")
    
    def upload(self, file_path: str, file_content: BinaryIO, metadata: dict = None) -> dict:
        """本地上传"""
        try:
            # 生成存储路径 (按日期分组)
            date_str = datetime.now().strftime("%Y/%m/%d")
            storage_dir = self.base_path / date_str
            storage_dir.mkdir(parents=True, exist_ok=True)
            
            # 保存文件
            full_path = storage_dir / file_path
            file_content.seek(0)
            file_size = 0
            with open(full_path, "wb") as f:
                while chunk := file_content.read(8192):
                    f.write(chunk)
                    file_size += len(chunk)
            
            # 推导 content_type
            content_type, _ = mimetypes.guess_type(str(full_path))
            content_type = content_type or "application/octet-stream"
            
            # 相对路径作为 key
            relative_key = str(full_path.relative_to(self.base_path))
            
            result = {
                "url": f"/static/uploads/{relative_key}",
                "key": relative_key,
                "size": file_size,
                "content_type": content_type,
                "uploaded_at": datetime.now().isoformat(),
                "storage_type": "local"
            }
            
            logger.info(f"File uploaded locally: {relative_key} ({file_size} bytes)")
            return result
            
        except Exception as e:
            logger.error(f"Local upload failed: {str(e)}")
            raise
    
    def download(self, file_key: str) -> BinaryIO:
        """本地下载"""
        try:
            full_path = self.base_path / file_key
            
            if not full_path.exists():
                raise FileNotFoundError(f"File not found: {file_key}")
            
            logger.info(f"File downloaded locally: {file_key}")
            return open(full_path, "rb")
            
        except Exception as e:
            logger.error(f"Local download failed: {str(e)}")
            raise
    
    def delete(self, file_key: str) -> bool:
        """本地删除"""
        try:
            full_path = self.base_path / file_key
            
            if full_path.exists():
                full_path.unlink()
                logger.info(f"File deleted locally: {file_key}")
                return True
            
            logger.warning(f"File not found for deletion: {file_key}")
            return False
            
        except Exception as e:
            logger.error(f"Local deletion failed: {str(e)}")
            raise
    
    def get_download_url(self, file_key: str, expires_in: int = 3600) -> str:
        """获取本地下载 URL（相对路径）"""
        return f"/static/uploads/{file_key}"
    
    def list_files(self, prefix: str = "", max_keys: int = 100) -> list:
        """列出本地文件"""
        try:
            files = []
            search_path = self.base_path / prefix if prefix else self.base_path
            
            if not search_path.exists():
                return files
            
            for file_path in list(search_path.rglob("*"))[:max_keys]:
                if file_path.is_file():
                    relative_key = str(file_path.relative_to(self.base_path))
                    files.append({
                        "key": relative_key,
                        "size": file_path.stat().st_size,
                        "modified_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
            
            logger.info(f"Listed {len(files)} local files")
            return sorted(files, key=lambda x: x.get("modified_at", ""), reverse=True)
            
        except Exception as e:
            logger.error(f"Local list failed: {str(e)}")
            raise
    
    def get_file_info(self, file_key: str) -> dict:
        """获取本地文件信息"""
        try:
            full_path = self.base_path / file_key
            
            if not full_path.exists():
                raise FileNotFoundError(f"File not found: {file_key}")
            
            stat = full_path.stat()
            content_type, _ = mimetypes.guess_type(str(full_path))
            
            return {
                "key": file_key,
                "size": stat.st_size,
                "content_type": content_type or "application/octet-stream",
                "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "url": f"/static/uploads/{file_key}"
            }
            
        except Exception as e:
            logger.error(f"Get file info failed: {str(e)}")
            raise


class S3StorageAdapter(CloudStorageAdapter):
    """AWS S3 存储适配器（存根实现，生产环境可扩展）"""
    
    def __init__(self, 
                 access_key: str = None, 
                 secret_key: str = None,
                 bucket: str = None, 
                 region: str = "us-east-1",
                 endpoint_url: str = None):
        """
        S3 初始化
        
        Args:
            access_key: AWS Access Key
            secret_key: AWS Secret Key
            bucket: S3 Bucket 名称
            region: AWS Region
            endpoint_url: 自定义端点（用于 MinIO 等兼容服务）
        """
        try:
            import boto3
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region,
                endpoint_url=endpoint_url
            )
            self.bucket = bucket
            logger.info(f"S3StorageAdapter initialized: bucket={bucket}, region={region}")
        except ImportError:
            logger.warning("boto3 not installed. S3 adapter will use stubs.")
            self.s3_client = None
    
    def upload(self, file_path: str, file_content: BinaryIO, metadata: dict = None) -> dict:
        """上传到 S3"""
        if not self.s3_client:
            logger.error("S3 client not available")
            raise RuntimeError("S3 adapter not configured")
        
        try:
            content_type, _ = mimetypes.guess_type(file_path)
            content_type = content_type or "application/octet-stream"
            
            # 使用日期前缀组织文件
            date_prefix = datetime.now().strftime("%Y/%m/%d")
            s3_key = f"{date_prefix}/{file_path}"
            
            file_content.seek(0)
            self.s3_client.upload_fileobj(
                file_content,
                self.bucket,
                s3_key,
                ExtraArgs={"ContentType": content_type, **(metadata or {})}
            )
            
            logger.info(f"File uploaded to S3: {s3_key}")
            
            return {
                "url": f"s3://{self.bucket}/{s3_key}",
                "key": s3_key,
                "bucket": self.bucket,
                "content_type": content_type,
                "uploaded_at": datetime.now().isoformat(),
                "storage_type": "s3"
            }
            
        except Exception as e:
            logger.error(f"S3 upload failed: {str(e)}")
            raise
    
    def download(self, file_key: str) -> BinaryIO:
        """从 S3 下载"""
        if not self.s3_client:
            raise RuntimeError("S3 adapter not configured")
        
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=file_key)
            logger.info(f"File downloaded from S3: {file_key}")
            return response["Body"]
        except Exception as e:
            logger.error(f"S3 download failed: {str(e)}")
            raise
    
    def delete(self, file_key: str) -> bool:
        """从 S3 删除"""
        if not self.s3_client:
            raise RuntimeError("S3 adapter not configured")
        
        try:
            self.s3_client.delete_object(Bucket=self.bucket, Key=file_key)
            logger.info(f"File deleted from S3: {file_key}")
            return True
        except Exception as e:
            logger.error(f"S3 deletion failed: {str(e)}")
            raise
    
    def get_download_url(self, file_key: str, expires_in: int = 3600) -> str:
        """获取 S3 预签名 URL"""
        if not self.s3_client:
            raise RuntimeError("S3 adapter not configured")
        
        try:
            url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": file_key},
                ExpiresIn=expires_in
            )
            logger.info(f"Generated S3 presigned URL: {file_key}")
            return url
        except Exception as e:
            logger.error(f"S3 URL generation failed: {str(e)}")
            raise
    
    def list_files(self, prefix: str = "", max_keys: int = 100) -> list:
        """列出 S3 文件"""
        if not self.s3_client:
            raise RuntimeError("S3 adapter not configured")
        
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket,
                Prefix=prefix,
                MaxKeys=max_keys
            )
            
            files = []
            for obj in response.get("Contents", []):
                files.append({
                    "key": obj["Key"],
                    "size": obj["Size"],
                    "modified_at": obj["LastModified"].isoformat()
                })
            
            logger.info(f"Listed {len(files)} S3 files")
            return files
            
        except Exception as e:
            logger.error(f"S3 list failed: {str(e)}")
            raise
    
    def get_file_info(self, file_key: str) -> dict:
        """获取 S3 文件信息"""
        if not self.s3_client:
            raise RuntimeError("S3 adapter not configured")
        
        try:
            response = self.s3_client.head_object(Bucket=self.bucket, Key=file_key)
            
            return {
                "key": file_key,
                "size": response["ContentLength"],
                "content_type": response.get("ContentType", "application/octet-stream"),
                "modified_at": response["LastModified"].isoformat(),
                "url": f"s3://{self.bucket}/{file_key}"
            }
            
        except Exception as e:
            logger.error(f"S3 get_file_info failed: {str(e)}")
            raise


class CloudStorageManager:
    """云存储管理器 - 工厂模式管理多个适配器"""
    
    def __init__(self, default_adapter: str = "local", **kwargs):
        """
        初始化存储管理器
        
        Args:
            default_adapter: 默认适配器类型 (local/s3)
            **kwargs: 传递给适配器的参数
        """
        self.adapters = {}
        self.default_adapter_name = default_adapter
        
        # 初始化本地适配器（始终可用）
        self.register_adapter("local", LocalStorageAdapter(**kwargs.get("local", {})))
        
        # 初始化 S3 适配器（如果配置）
        if "s3" in kwargs:
            try:
                self.register_adapter("s3", S3StorageAdapter(**kwargs.get("s3", {})))
            except Exception as e:
                logger.warning(f"S3 adapter registration failed: {str(e)}")
        
        logger.info(f"CloudStorageManager initialized with default={default_adapter}")
    
    def register_adapter(self, name: str, adapter: CloudStorageAdapter):
        """注册存储适配器"""
        self.adapters[name] = adapter
        logger.info(f"Storage adapter registered: {name}")
    
    def get_adapter(self, adapter_name: str = None) -> CloudStorageAdapter:
        """获取存储适配器"""
        name = adapter_name or self.default_adapter_name
        
        if name not in self.adapters:
            raise ValueError(f"Unknown adapter: {name}")
        
        return self.adapters[name]
    
    def upload(self, file_path: str, file_content: BinaryIO, 
               adapter_name: str = None, metadata: dict = None) -> dict:
        """上传文件"""
        adapter = self.get_adapter(adapter_name)
        return adapter.upload(file_path, file_content, metadata)
    
    def download(self, file_key: str, adapter_name: str = None) -> BinaryIO:
        """下载文件"""
        adapter = self.get_adapter(adapter_name)
        return adapter.download(file_key)
    
    def delete(self, file_key: str, adapter_name: str = None) -> bool:
        """删除文件"""
        adapter = self.get_adapter(adapter_name)
        return adapter.delete(file_key)
    
    def get_download_url(self, file_key: str, adapter_name: str = None, expires_in: int = 3600) -> str:
        """获取下载 URL"""
        adapter = self.get_adapter(adapter_name)
        return adapter.get_download_url(file_key, expires_in)
    
    def list_files(self, prefix: str = "", adapter_name: str = None, max_keys: int = 100) -> list:
        """列出文件"""
        adapter = self.get_adapter(adapter_name)
        return adapter.list_files(prefix, max_keys)
    
    def get_file_info(self, file_key: str, adapter_name: str = None) -> dict:
        """获取文件信息"""
        adapter = self.get_adapter(adapter_name)
        return adapter.get_file_info(file_key)


# 全局单例
_storage_manager: Optional[CloudStorageManager] = None


def get_storage_manager(default_adapter: str = "local", **kwargs) -> CloudStorageManager:
    """获取全局存储管理器（单例）"""
    global _storage_manager
    
    if _storage_manager is None:
        _storage_manager = CloudStorageManager(default_adapter=default_adapter, **kwargs)
    
    return _storage_manager
