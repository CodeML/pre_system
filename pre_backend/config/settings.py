import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/pre_system.db")
# JWT配置
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))
# 文件配置
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./static/uploads")
# 跨域配置
CORS_ORIGINS = ["*"]
# 服务端口
PORT = int(os.getenv("PORT", 8000))
