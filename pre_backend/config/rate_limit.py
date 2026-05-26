from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict

from config.config import settings

# 简单的基于内存的 IP 限流器
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.ip_records = defaultdict(list)
        self.limit = settings.RATE_LIMIT_PER_MINUTE
        self.window = 60

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        
        # 清理过期记录
        self.ip_records[client_ip] = [
            timestamp for timestamp in self.ip_records[client_ip]
            if current_time - timestamp < self.window
        ]
        
        # 检查是否超限
        if len(self.ip_records[client_ip]) >= self.limit:
            raise HTTPException(status_code=429, detail="Too Many Requests. 请稍后再试。")
            
        self.ip_records[client_ip].append(current_time)
        
        response = await call_next(request)
        return response
