from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # 基础配置
    PROJECT_NAME: str = "设计工作室PRE系统"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # 数据库
    DATABASE_URL: str = "sqlite:///./pre_system.db"
    
    # 安全
    SECRET_KEY: str = "your-secret-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7天
    
    # SaaS 阈值
    RATE_LIMIT_PER_MINUTE: int = 100
    SLOW_REQUEST_THRESHOLD: float = 0.5 # 秒
    
    # 日志
    LOG_LEVEL: str = "INFO"
    ENABLE_AUDIT_LOG: bool = True
    
    # 缓存 (Redis)
    REDIS_URL: Optional[str] = None
    
    # 存储 (OSS/S3)
    STORAGE_TYPE: str = "local" # local / s3
    UPLOAD_DIR: str = "static/uploads"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
