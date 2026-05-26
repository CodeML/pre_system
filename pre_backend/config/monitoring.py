import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("pre_system.monitoring")

class MonitoringMiddleware(BaseHTTPMiddleware):
    """
    性能监控中间件
    记录每个接口的响应时间，为后续接入 Prometheus 做准备
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # 处理请求
        response = await call_next(request)
        
        # 计算耗时
        process_time = time.time() - start_time
        
        # 记录慢日志（超过 500ms 的请求）
        if process_time > 0.5:
            logger.warning(
                f"Slow Request: {request.method} {request.url.path} "
                f"took {process_time:.4f}s | IP: {request.client.host}"
            )
        
        # 在响应头中加入处理时间（方便前端调试）
        response.headers["X-Process-Time"] = str(process_time)
        return response
