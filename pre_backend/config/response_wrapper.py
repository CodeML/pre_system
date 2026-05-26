import time
import uuid
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from config.config import settings

logger = logging.getLogger("pre_system.core")

class UnifiedResponseMiddleware(BaseHTTPMiddleware):
    """
    1. 生成全局唯一 TraceID
    2. 统一接口返回结构
    3. 监控响应时间
    """
    async def dispatch(self, request: Request, call_next):
        # 1. 生成或提取 TraceID
        trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
        request.state.trace_id = trace_id
        
        start_time = time.time()
        
        try:
            # 2. 执行后续逻辑
            response = await call_next(request)
            
            # 3. 性能监控
            process_time = time.time() - start_time
            if process_time > settings.SLOW_REQUEST_THRESHOLD:
                logger.warning(f"[{trace_id}] Slow Request: {request.method} {request.url.path} took {process_time:.4f}s")
            
            # 4. 注入 TraceID 到响应头
            response.headers["X-Trace-ID"] = trace_id
            response.headers["X-Process-Time"] = str(process_time)
            
            return response

        except Exception as exc:
            # 全局异常捕获，确保返回结构统一
            process_time = time.time() - start_time
            logger.error(f"[{trace_id}] Unhandled Exception: {str(exc)}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "code": 500,
                    "data": None,
                    "message": f"系统内部错误: {str(exc)}",
                    "trace_id": trace_id
                }
            )

def wrap_response(data=None, code=200, message="success", trace_id=""):
    """
    手动包装返回结构的辅助函数
    """
    return {
        "code": code,
        "data": data,
        "message": message,
        "trace_id": trace_id
    }
