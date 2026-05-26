import json
from typing import Optional, Any
from datetime import timedelta

class CacheManager:
    """
    缓存管理器抽象
    默认为内存缓存，可轻松切换为 Redis
    """
    _instance = None
    _data = {} # 内存存储

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CacheManager, cls).__new__(cls)
        return cls._instance

    def set(self, key: str, value: Any, expire: int = 3600):
        """写入缓存"""
        # 实际生产环境：self.redis.set(key, json.dumps(value), ex=expire)
        self._data[key] = {
            "value": value,
            "expire_at": time.time() + expire if expire else None
        }

    def get(self, key: str) -> Optional[Any]:
        """读取缓存"""
        if key not in self._data:
            return None
        
        item = self._data[key]
        if item["expire_at"] and time.time() > item["expire_at"]:
            del self._data[key]
            return None
            
        return item["value"]

    def delete(self, key: str):
        """删除缓存"""
        if key in self._data:
            del self._data[key]

    def acquire_lock(self, lock_name: str, expire: int = 10) -> bool:
        """
        获取分布式锁（内存模拟实现）
        """
        key = f"lock:{lock_name}"
        if key in self._data:
            item = self._data[key]
            if item["expire_at"] and time.time() < item["expire_at"]:
                return False # 锁已被占用且未过期
        
        # 加锁
        self.set(key, "locked", expire=expire)
        return True

    def release_lock(self, lock_name: str):
        """释放锁"""
        self.delete(f"lock:{lock_name}")

# 全局单例
cache = CacheManager()
import time # 用于上面的 time.time()
