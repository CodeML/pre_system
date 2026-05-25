from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from api import register_routers
from database.db import init_db
from config.exceptions import AppException, create_exception_handlers
from config.logger_advanced import get_logger

# 初始化日志
logger = get_logger()

# 初始化FastAPI
app = FastAPI(title="设计工作室PRE系统", version="1.0.0")

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有，生产环境替换为前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册全局异常处理器
exception_handlers = create_exception_handlers()
for exc_type, handler in exception_handlers.items():
    app.add_exception_handler(exc_type, handler)

# 注册路由
register_routers(app)

# 初始化数据库
@app.on_event("startup")
async def startup_event():
    init_db()
    logger.info("✅ Application started - Database initialized")

# 测试接口
@app.get("/")
async def root():
    return {"message": "PRE系统后端启动成功"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
