#!/usr/bin/env python3
"""
第三阶段验证脚本
验证云存储、缓存、日志、速率限制等功能
"""

import sys
from pathlib import Path
from io import BytesIO

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from config.logger_advanced import get_logger
from utils.cloud_storage import get_storage_manager, LocalStorageAdapter
from utils.cache_manager import get_cache_manager, CacheManager, cached, cache_key
from config.rate_limit import RateLimiter

logger = get_logger()

def test_logger():
    """测试日志系统"""
    print("\n" + "="*60)
    print("TEST 1: Logger System")
    print("="*60)
    
    try:
        logger.debug("Debug message test")
        logger.info("Info message test")
        logger.warning("Warning message test")
        logger.error("Error message test")
        
        print("✅ Logger system working")
        return True
    except Exception as e:
        print(f"❌ Logger test failed: {str(e)}")
        return False


def test_local_storage():
    """测试本地存储"""
    print("\n" + "="*60)
    print("TEST 2: Local Storage")
    print("="*60)
    
    try:
        # 获取存储管理器
        manager = get_storage_manager(default_adapter="local")
        
        # 上传测试文件
        test_content = b"Hello, Cloud Storage!"
        file_obj = BytesIO(test_content)
        
        result = manager.upload("test_file.txt", file_obj)
        print(f"✅ Upload result: {result}")
        
        # 检查文件信息
        file_info = manager.get_file_info(result["key"])
        print(f"✅ File info: {file_info}")
        
        # 获取下载 URL
        download_url = manager.get_download_url(result["key"])
        print(f"✅ Download URL: {download_url}")
        
        # 列出文件
        files = manager.list_files()
        print(f"✅ Listed {len(files)} files")
        
        # 删除文件
        deleted = manager.delete(result["key"])
        print(f"✅ File deleted: {deleted}")
        
        return True
    except Exception as e:
        print(f"❌ Storage test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_memory_cache():
    """测试内存缓存"""
    print("\n" + "="*60)
    print("TEST 3: Memory Cache")
    print("="*60)
    
    try:
        manager = get_cache_manager(backend_type="memory")
        
        # 设置缓存
        manager.set("key1", "value1", ttl=60)
        print("✅ Cache set: key1=value1")
        
        # 获取缓存
        value = manager.get("key1")
        assert value == "value1", f"Expected 'value1', got {value}"
        print(f"✅ Cache get: key1={value}")
        
        # 检查存在性
        exists = manager.exists("key1")
        assert exists, "Key should exist"
        print(f"✅ Cache exists: key1={exists}")
        
        # 递增
        manager.set("counter", 0)
        new_value = manager.increment("counter", 5)
        assert new_value == 5, f"Expected 5, got {new_value}"
        print(f"✅ Cache increment: counter={new_value}")
        
        # 递减
        new_value = manager.decrement("counter", 2)
        assert new_value == 3, f"Expected 3, got {new_value}"
        print(f"✅ Cache decrement: counter={new_value}")
        
        # 获取 TTL
        ttl = manager.get_ttl("key1")
        assert ttl > 0, f"Expected positive TTL, got {ttl}"
        print(f"✅ Cache TTL: key1={ttl}s")
        
        # 删除缓存
        deleted = manager.delete("key1")
        assert deleted, "Delete should return True"
        print(f"✅ Cache deleted: key1")
        
        # 清空缓存
        manager.clear()
        print("✅ Cache cleared")
        
        return True
    except Exception as e:
        print(f"❌ Cache test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_cache_decorator():
    """测试缓存装饰器"""
    print("\n" + "="*60)
    print("TEST 4: Cache Decorator")
    print("="*60)
    
    try:
        # 重置缓存管理器
        global _cache_manager
        import utils.cache_manager
        utils.cache_manager._cache_manager = None
        
        call_count = 0
        
        @cached(ttl=600)
        def expensive_function(user_id):
            nonlocal call_count
            call_count += 1
            return f"user_{user_id}_data"
        
        # 第一次调用
        result1 = expensive_function(123)
        print(f"✅ First call: {result1}, call_count={call_count}")
        assert call_count == 1, f"Expected 1 call, got {call_count}"
        
        # 第二次调用（应该从缓存获取）
        result2 = expensive_function(123)
        print(f"✅ Second call (cached): {result2}, call_count={call_count}")
        assert call_count == 1, f"Expected 1 call (cached), got {call_count}"
        assert result1 == result2, "Results should be the same"
        
        # 不同参数
        result3 = expensive_function(456)
        print(f"✅ Third call (different param): {result3}, call_count={call_count}")
        assert call_count == 2, f"Expected 2 calls, got {call_count}"
        
        return True
    except Exception as e:
        print(f"❌ Cache decorator test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_rate_limiter():
    """测试速率限制"""
    print("\n" + "="*60)
    print("TEST 5: Rate Limiter")
    print("="*60)
    
    try:
        limiter = RateLimiter()
        
        # 前 5 次请求应该通过
        user_id = 123
        for i in range(5):
            allowed, info = limiter.check_user_limit(user_id, limit=5, window_seconds=60)
            print(f"✅ Request {i+1}: allowed={allowed}, remaining={info.get('remaining', 0)}")
            assert allowed, f"Request {i+1} should be allowed"
        
        # 第 6 次请求应该被限制
        allowed, info = limiter.check_user_limit(user_id, limit=5, window_seconds=60)
        print(f"✅ Request 6 (rate limited): allowed={allowed}, remaining={info.get('remaining', 0)}")
        assert not allowed, "Request 6 should be rate limited"
        
        return True
    except Exception as e:
        print(f"❌ Rate limiter test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_cache_key_generation():
    """测试缓存 key 生成"""
    print("\n" + "="*60)
    print("TEST 6: Cache Key Generation")
    print("="*60)
    
    try:
        key1 = cache_key("user", 123, status="active")
        print(f"✅ Generated key: {key1}")
        
        # 相同参数应该生成相同的 key
        key2 = cache_key("user", 123, status="active")
        assert key1 == key2, f"Keys should be the same: {key1} != {key2}"
        print(f"✅ Same parameters produce same key")
        
        # 不同参数应该生成不同的 key
        key3 = cache_key("user", 456, status="active")
        assert key1 != key3, f"Keys should be different: {key1} == {key3}"
        print(f"✅ Different parameters produce different keys")
        
        return True
    except Exception as e:
        print(f"❌ Cache key generation test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("PRE系统 - 第三阶段验证")
    print("="*60)
    
    tests = [
        ("Logger System", test_logger),
        ("Local Storage", test_local_storage),
        ("Memory Cache", test_memory_cache),
        ("Cache Decorator", test_cache_decorator),
        ("Rate Limiter", test_rate_limiter),
        ("Cache Key Generation", test_cache_key_generation),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} crashed: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # 汇总
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
