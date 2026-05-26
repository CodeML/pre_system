from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from api import register_routers
from database.db import init_db
from config.config import settings
from config.exceptions import AppException, create_exception_handlers
from config.logger_advanced import get_logger
from config.rate_limit import RateLimitMiddleware
from config.monitoring import MonitoringMiddleware
from config.response_wrapper import UnifiedResponseMiddleware
from config.scheduler import start_scheduler

# 初始化日志
logger = get_logger()

# 初始化FastAPI
app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# 1. 注册路由 (放在最内层)
register_routers(app)

# 2. 注册全局异常处理器
exception_handlers = create_exception_handlers()
for exc_type, handler in exception_handlers.items():
    app.add_exception_handler(exc_type, handler)

# 3. SaaS 增强中间件 (按照过滤顺序：越晚添加的越在外层)
# 响应统一包装 -> 性能监控 -> 限流 -> CORS
app.add_middleware(UnifiedResponseMiddleware)
app.add_middleware(MonitoringMiddleware)
app.add_middleware(RateLimitMiddleware)

# CORS 必须放在最外层，确保即便中间件报错也能带上跨域头
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8081", "http://localhost:8081", "http://0.0.0.0:8081"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
@app.on_event("startup")
async def startup_event():
    init_db()
    # 启动后台定时任务
    start_scheduler()
    logger.info(f"✅ Application {settings.PROJECT_NAME} started - Database initialized")

# 测试接口
@app.get("/")
async def root():
    return {"message": f"{settings.PROJECT_NAME}后端启动成功"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=settings.DEBUG)
