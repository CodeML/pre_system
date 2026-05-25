"""
API 速率限制系统
支持基于用户和 IP 的限制
"""

from typing import Dict, Tuple
from datetime import datetime, timedelta
from functools import wraps
from fastapi import HTTPException, Request
import time


class RateLimiter:
    """速率限制器（内存存储版本，生产环境建议用 Redis）"""
    
    def __init__(self):
        self.users = {}  # {user_id: [(timestamp, count), ...]}
        self.ips = {}    # {ip: [(timestamp, count), ...]}
    
    def _cleanup_old_entries(self, entries: list, window_seconds: int):
        """清理超过时间窗口的记录"""
        cutoff = time.time() - window_seconds
        return [e for e in entries if e[0] > cutoff]
    
    def check_user_limit(self, user_id: int, 
                        limit: int = 100, 
                        window_seconds: int = 60) -> Tuple[bool, Dict]:
        """
        检查用户是否超过限制
        
        Args:
            user_id: 用户 ID
            limit: 时间窗口内允许的请求数
            window_seconds: 时间窗口（秒）
        
        Returns:
            (是否通过, 限制信息字典)
        """
        now = time.time()
        key = f"user_{user_id}"
        
        if key not in self.users:
            self.users[key] = []
        
        # 清理旧记录
        self.users[key] = self._cleanup_old_entries(self.users[key], window_seconds)
        
        # 检查限制
        if len(self.users[key]) >= limit:
            oldest_timestamp = self.users[key][0][0]
            reset_in = int(window_seconds - (now - oldest_timestamp))
            return False, {
                "limit": limit,
                "remaining": 0,
                "reset_in_seconds": max(0, reset_in)
            }
        
        # 添加当前请求
        self.users[key].append((now, 1))
        remaining = limit - len(self.users[key])
        
        return True, {
            "limit": limit,
            "remaining": remaining,
            "reset_in_seconds": window_seconds
        }
    
    def check_ip_limit(self, ip: str, 
                       limit: int = 200, 
                       window_seconds: int = 60) -> Tuple[bool, Dict]:
        """
        检查 IP 是否超过限制
        
        Args:
            ip: 客户端 IP 地址
            limit: 时间窗口内允许的请求数
            window_seconds: 时间窗口（秒）
        
        Returns:
            (是否通过, 限制信息字典)
        """
        now = time.time()
        
        if ip not in self.ips:
            self.ips[ip] = []
        
        # 清理旧记录
        self.ips[ip] = self._cleanup_old_entries(self.ips[ip], window_seconds)
        
        # 检查限制
        if len(self.ips[ip]) >= limit:
            oldest_timestamp = self.ips[ip][0][0]
            reset_in = int(window_seconds - (now - oldest_timestamp))
            return False, {
                "limit": limit,
                "remaining": 0,
                "reset_in_seconds": max(0, reset_in)
            }
        
        # 添加当前请求
        self.ips[ip].append((now, 1))
        remaining = limit - len(self.ips[ip])
        
        return True, {
            "limit": limit,
            "remaining": remaining,
            "reset_in_seconds": window_seconds
        }
    
    def reset_user(self, user_id: int):
        """重置用户限制"""
        key = f"user_{user_id}"
        if key in self.users:
            del self.users[key]
    
    def reset_ip(self, ip: str):
        """重置 IP 限制"""
        if ip in self.ips:
            del self.ips[ip]


# 全局速率限制器实例
_rate_limiter = RateLimiter()


def get_rate_limiter() -> RateLimiter:
    """获取全局速率限制器"""
    return _rate_limiter


def require_rate_limit(user_limit: int = 100, 
                      user_window: int = 60,
                      ip_limit: int = 200, 
                      ip_window: int = 60):
    """
    装饰器：检查 API 速率限制
    
    Args:
        user_limit: 用户每个时间窗口允许的请求数
        user_window: 用户时间窗口（秒）
        ip_limit: IP 每个时间窗口允许的请求数
        ip_window: IP 时间窗口（秒）
    
    用法:
        @router.get("/api/resource")
        @require_rate_limit(user_limit=100, user_window=60)
        def get_resource(request: Request, current_user: User = Depends(get_current_user)):
            return {"data": "..."}
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            limiter = get_rate_limiter()
            
            # 获取客户端 IP
            client_ip = request.client.host if request.client else "unknown"
            
            # 获取当前用户
            current_user = kwargs.get('current_user')
            user_id = current_user.id if current_user else None
            
            # 检查 IP 限制
            ip_passed, ip_info = limiter.check_ip_limit(client_ip, ip_limit, ip_window)
            if not ip_passed:
                raise HTTPException(
                    status_code=429,
                    detail=f"Too many requests from IP {client_ip}. Reset in {ip_info['reset_in_seconds']}s"
                )
            
            # 检查用户限制
            if user_id:
                user_passed, user_info = limiter.check_user_limit(user_id, user_limit, user_window)
                if not user_passed:
                    raise HTTPException(
                        status_code=429,
                        detail=f"User request limit exceeded. Reset in {user_info['reset_in_seconds']}s"
                    )
            
            # 调用原函数
            return await func(request, *args, **kwargs)
        
        return wrapper
    return decorator


# 便利函数：获取限制状态信息
def get_rate_limit_status(user_id: int = None, ip: str = None) -> Dict:
    """获取速率限制状态"""
    limiter = get_rate_limiter()
    status = {}
    
    if user_id:
        _, user_info = limiter.check_user_limit(user_id)
        status["user"] = user_info
    
    if ip:
        _, ip_info = limiter.check_ip_limit(ip)
        status["ip"] = ip_info
    
    return status
