"""
缓存管理器 - 支持 Redis 和内存缓存
提供统一的缓存接口，支持多后端
"""

from abc import ABC, abstractmethod
from typing import Optional, Any, Union
from datetime import datetime, timedelta
import json
import pickle
from config.logger_advanced import get_logger

logger = get_logger()


class CacheBackend(ABC):
    """缓存后端基类"""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """设置缓存值"""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """删除缓存"""
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        pass
    
    @abstractmethod
    def clear(self) -> bool:
        """清空缓存"""
        pass
    
    @abstractmethod
    def get_ttl(self, key: str) -> int:
        """获取剩余 TTL（秒），-1 永久，-2 不存在"""
        pass
    
    @abstractmethod
    def increment(self, key: str, amount: int = 1) -> int:
        """递增计数"""
        pass
    
    @abstractmethod
    def decrement(self, key: str, amount: int = 1) -> int:
        """递减计数"""
        pass


class MemoryCacheBackend(CacheBackend):
    """内存缓存后端"""
    
    def __init__(self):
        self.cache: dict = {}
        self.expiry: dict = {}
        logger.info("MemoryCacheBackend initialized")
    
    def _cleanup_expired(self, key: str) -> None:
        """清理过期缓存"""
        if key in self.expiry:
            if datetime.now() > self.expiry[key]:
                self.cache.pop(key, None)
                self.expiry.pop(key, None)
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        self._cleanup_expired(key)
        return self.cache.get(key)
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """设置缓存"""
        try:
            self.cache[key] = value
            self.expiry[key] = datetime.now() + timedelta(seconds=ttl)
            logger.debug(f"Cache set: {key} (ttl={ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Cache set failed: {key} - {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        try:
            self.cache.pop(key, None)
            self.expiry.pop(key, None)
            logger.debug(f"Cache deleted: {key}")
            return True
        except Exception as e:
            logger.error(f"Cache delete failed: {key} - {str(e)}")
            return False
    
    def exists(self, key: str) -> bool:
        """检查是否存在"""
        self._cleanup_expired(key)
        return key in self.cache
    
    def clear(self) -> bool:
        """清空缓存"""
        try:
            self.cache.clear()
            self.expiry.clear()
            logger.info("Cache cleared")
            return True
        except Exception as e:
            logger.error(f"Cache clear failed: {str(e)}")
            return False
    
    def get_ttl(self, key: str) -> int:
        """获取 TTL"""
        self._cleanup_expired(key)
        
        if key not in self.cache:
            return -2  # 不存在
        
        if key not in self.expiry:
            return -1  # 永久
        
        remaining = (self.expiry[key] - datetime.now()).total_seconds()
        return max(0, int(remaining))
    
    def increment(self, key: str, amount: int = 1) -> int:
        """递增"""
        try:
            self._cleanup_expired(key)
            current = self.cache.get(key, 0)
            new_value = int(current) + amount
            self.cache[key] = new_value
            logger.debug(f"Cache incremented: {key} -> {new_value}")
            return new_value
        except Exception as e:
            logger.error(f"Cache increment failed: {key} - {str(e)}")
            return 0
    
    def decrement(self, key: str, amount: int = 1) -> int:
        """递减"""
        try:
            self._cleanup_expired(key)
            current = self.cache.get(key, 0)
            new_value = int(current) - amount
            self.cache[key] = new_value
            logger.debug(f"Cache decremented: {key} -> {new_value}")
            return new_value
        except Exception as e:
            logger.error(f"Cache decrement failed: {key} - {str(e)}")
            return 0


class RedisCacheBackend(CacheBackend):
    """Redis 缓存后端"""
    
    def __init__(self, host: str = "localhost", port: int = 6379, 
                 db: int = 0, password: str = None, decode_responses: bool = True):
        """
        Redis 初始化
        
        Args:
            host: Redis 主机
            port: Redis 端口
            db: Redis 数据库索引
            password: Redis 密码
            decode_responses: 是否返回字符串
        """
        try:
            import redis
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=decode_responses,
                socket_connect_timeout=5,
                socket_keepalive=True
            )
            
            # 测试连接
            self.redis_client.ping()
            logger.info(f"RedisCacheBackend connected: {host}:{port}")
            
        except ImportError:
            logger.warning("redis not installed. Redis backend will use stubs.")
            self.redis_client = None
        except Exception as e:
            logger.warning(f"Redis connection failed: {str(e)}. Will use stubs.")
            self.redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if not self.redis_client:
            logger.warning("Redis client not available")
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                # 尝试反序列化
                try:
                    return json.loads(value)
                except:
                    return value
            return None
        except Exception as e:
            logger.error(f"Redis get failed: {key} - {str(e)}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """设置缓存"""
        if not self.redis_client:
            logger.warning("Redis client not available")
            return False
        
        try:
            # 序列化值
            if not isinstance(value, str):
                value = json.dumps(value, default=str)
            
            self.redis_client.setex(key, ttl, value)
            logger.debug(f"Redis set: {key} (ttl={ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Redis set failed: {key} - {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        if not self.redis_client:
            logger.warning("Redis client not available")
            return False
        
        try:
            self.redis_client.delete(key)
            logger.debug(f"Redis deleted: {key}")
            return True
        except Exception as e:
            logger.error(f"Redis delete failed: {key} - {str(e)}")
            return False
    
    def exists(self, key: str) -> bool:
        """检查是否存在"""
        if not self.redis_client:
            logger.warning("Redis client not available")
            return False
        
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"Redis exists failed: {key} - {str(e)}")
            return False
    
    def clear(self) -> bool:
        """清空缓存"""
        if not self.redis_client:
            logger.warning("Redis client not available")
            return False
        
        try:
            self.redis_client.flushdb()
            logger.info("Redis cleared")
            return True
        except Exception as e:
            logger.error(f"Redis clear failed: {str(e)}")
            return False
    
    def get_ttl(self, key: str) -> int:
        """获取 TTL"""
        if not self.redis_client:
            logger.warning("Redis client not available")
            return -2
        
        try:
            ttl = self.redis_client.ttl(key)
            return ttl  # -1: 永久，-2: 不存在
        except Exception as e:
            logger.error(f"Redis TTL failed: {key} - {str(e)}")
            return -2
    
    def increment(self, key: str, amount: int = 1) -> int:
        """递增"""
        if not self.redis_client:
            logger.warning("Redis client not available")
            return 0
        
        try:
            new_value = self.redis_client.incr(key, amount)
            logger.debug(f"Redis incremented: {key} -> {new_value}")
            return new_value
        except Exception as e:
            logger.error(f"Redis increment failed: {key} - {str(e)}")
            return 0
    
    def decrement(self, key: str, amount: int = 1) -> int:
        """递减"""
        if not self.redis_client:
            logger.warning("Redis client not available")
            return 0
        
        try:
            new_value = self.redis_client.decr(key, amount)
            logger.debug(f"Redis decremented: {key} -> {new_value}")
            return new_value
        except Exception as e:
            logger.error(f"Redis decrement failed: {key} - {str(e)}")
            return 0


class CacheManager:
    """缓存管理器 - 统一缓存接口"""
    
    def __init__(self, backend_type: str = "memory", **kwargs):
        """
        初始化缓存管理器
        
        Args:
            backend_type: 后端类型 (memory/redis)
            **kwargs: 传递给后端的参数
        """
        self.backend_type = backend_type
        
        if backend_type == "redis":
            try:
                self.backend = RedisCacheBackend(**kwargs.get("redis", {}))
            except Exception as e:
                logger.warning(f"Redis backend failed, falling back to memory: {str(e)}")
                self.backend = MemoryCacheBackend()
        else:
            self.backend = MemoryCacheBackend()
        
        logger.info(f"CacheManager initialized with {self.backend.__class__.__name__}")
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        return self.backend.get(key)
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """设置缓存"""
        return self.backend.set(key, value, ttl)
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        return self.backend.delete(key)
    
    def exists(self, key: str) -> bool:
        """检查是否存在"""
        return self.backend.exists(key)
    
    def clear(self) -> bool:
        """清空缓存"""
        return self.backend.clear()
    
    def get_ttl(self, key: str) -> int:
        """获取 TTL"""
        return self.backend.get_ttl(key)
    
    def increment(self, key: str, amount: int = 1) -> int:
        """递增计数"""
        return self.backend.increment(key, amount)
    
    def decrement(self, key: str, amount: int = 1) -> int:
        """递减计数"""
        return self.backend.decrement(key, amount)
    
    def get_or_set(self, key: str, value_fn, ttl: int = 3600) -> Any:
        """获取或设置（惰性加载）"""
        value = self.get(key)
        
        if value is None:
            value = value_fn()
            if value is not None:
                self.set(key, value, ttl)
        
        return value
    
    def invalidate_pattern(self, pattern: str) -> int:
        """
        按模式删除缓存（Redis only）
        
        Args:
            pattern: Redis 模式 (如 "user:*")
        
        Returns:
            删除的 key 数量
        """
        if not isinstance(self.backend, RedisCacheBackend):
            logger.warning("Pattern invalidation only supported by Redis backend")
            return 0
        
        try:
            keys = self.backend.redis_client.keys(pattern)
            if keys:
                self.backend.redis_client.delete(*keys)
                logger.info(f"Invalidated {len(keys)} keys matching pattern: {pattern}")
            return len(keys)
        except Exception as e:
            logger.error(f"Pattern invalidation failed: {str(e)}")
            return 0


# 全局单例
_cache_manager: Optional[CacheManager] = None


def get_cache_manager(backend_type: str = "memory", **kwargs) -> CacheManager:
    """获取全局缓存管理器（单例）"""
    global _cache_manager
    
    if _cache_manager is None:
        _cache_manager = CacheManager(backend_type=backend_type, **kwargs)
    
    return _cache_manager


def cache_key(*args, **kwargs) -> str:
    """生成缓存 key"""
    parts = []
    
    # 添加位置参数
    for arg in args:
        parts.append(str(arg))
    
    # 添加关键字参数（排序以保证一致性）
    for k, v in sorted(kwargs.items()):
        parts.append(f"{k}:{v}")
    
    return ":".join(parts)


def cached(ttl: int = 3600, key_fn=None):
    """
    缓存装饰器
    
    Args:
        ttl: 缓存时间（秒）
        key_fn: 自定义 key 生成函数
    
    Usage:
        @cached(ttl=600)
        def get_user(user_id):
            return fetch_user_from_db(user_id)
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 生成缓存 key
            if key_fn:
                cache_k = key_fn(*args, **kwargs)
            else:
                cache_k = cache_key(func.__name__, *args, **kwargs)
            
            # 获取缓存
            manager = get_cache_manager()
            cached_value = manager.get(cache_k)
            
            if cached_value is not None:
                logger.debug(f"Cache hit: {cache_k}")
                return cached_value
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 存储缓存
            manager.set(cache_k, result, ttl)
            logger.debug(f"Cache set: {cache_k} (ttl={ttl}s)")
            
            return result
        
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    
    return decorator
