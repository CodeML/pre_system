#!/usr/bin/env python3
"""
第三阶段 3.5 - 生产部署测试
完整的系统集成测试、性能基准和安全检查
"""

import sys
import time
import json
import requests
import statistics
from pathlib import Path
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple

# 配置
API_BASE_URL = "http://127.0.0.1:8000"
SWAGGER_URL = f"{API_BASE_URL}/docs"
TEST_TIMEOUT = 10


class ProductionTestSuite:
    """生产环境测试套件"""
    
    def __init__(self):
        self.results = []
        self.performance_data = {}
    
    def log_result(self, test_name: str, passed: bool, message: str = "", duration: float = 0):
        """记录测试结果"""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        print(f"{status}: {test_name} ({duration:.3f}s)" + (f" - {message}" if message else ""))
    
    def test_api_availability(self) -> bool:
        """测试 API 可用性"""
        print("\n" + "="*60)
        print("TEST 1: API Availability")
        print("="*60)
        
        try:
            start = time.time()
            response = requests.get(f"{API_BASE_URL}/", timeout=TEST_TIMEOUT)
            duration = time.time() - start
            
            passed = response.status_code == 200
            self.log_result("Root endpoint", passed, f"Status: {response.status_code}", duration)
            
            return passed
        except Exception as e:
            self.log_result("Root endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_swagger_ui(self) -> bool:
        """测试 Swagger UI 可访问性"""
        print("\n" + "="*60)
        print("TEST 2: Swagger UI & OpenAPI Schema")
        print("="*60)
        
        try:
            # 检查 Swagger UI
            start = time.time()
            response = requests.get(SWAGGER_URL, timeout=TEST_TIMEOUT)
            duration_swagger = time.time() - start
            swagger_ok = response.status_code == 200
            self.log_result("Swagger UI available", swagger_ok, f"Status: {response.status_code}", duration_swagger)
            
            # 检查 OpenAPI schema
            start = time.time()
            response = requests.get(f"{API_BASE_URL}/openapi.json", timeout=TEST_TIMEOUT)
            duration_schema = time.time() - start
            schema_ok = response.status_code == 200
            
            if schema_ok:
                schema = response.json()
                endpoint_count = len(schema.get("paths", {}))
                self.log_result(
                    "OpenAPI schema available",
                    True,
                    f"Status: 200, Endpoints: {endpoint_count}",
                    duration_schema
                )
            else:
                self.log_result("OpenAPI schema available", False, f"Status: {response.status_code}", duration_schema)
            
            return swagger_ok and schema_ok
        except Exception as e:
            self.log_result("Swagger/OpenAPI", False, f"Error: {str(e)}")
            return False
    
    def test_error_handling(self) -> bool:
        """测试全局异常处理"""
        print("\n" + "="*60)
        print("TEST 3: Error Handling & Exception Format")
        print("="*60)
        
        all_passed = True
        
        # 测试 404
        try:
            start = time.time()
            response = requests.get(f"{API_BASE_URL}/api/nonexistent", timeout=TEST_TIMEOUT)
            duration = time.time() - start
            
            passed = response.status_code == 404
            self.log_result("404 Not Found", passed, f"Status: {response.status_code}", duration)
            all_passed = all_passed and passed
        except Exception as e:
            self.log_result("404 Not Found", False, f"Error: {str(e)}")
            all_passed = False
        
        # 测试无效方法
        try:
            start = time.time()
            response = requests.post(f"{API_BASE_URL}/", timeout=TEST_TIMEOUT)
            duration = time.time() - start
            
            passed = response.status_code in [405, 422]  # Method Not Allowed 或 Unprocessable Entity
            self.log_result("Invalid Method Handling", passed, f"Status: {response.status_code}", duration)
            all_passed = all_passed and passed
        except Exception as e:
            self.log_result("Invalid Method Handling", False, f"Error: {str(e)}")
            all_passed = False
        
        return all_passed
    
    def test_cors_headers(self) -> bool:
        """测试 CORS 头设置"""
        print("\n" + "="*60)
        print("TEST 4: CORS Headers")
        print("="*60)
        
        try:
            start = time.time()
            response = requests.get(
                f"{API_BASE_URL}/",
                headers={"Origin": "http://localhost:3000"},
                timeout=TEST_TIMEOUT
            )
            duration = time.time() - start
            
            has_cors = "access-control-allow-origin" in response.headers
            self.log_result(
                "CORS headers present",
                has_cors,
                f"CORS: {response.headers.get('access-control-allow-origin', 'Not set')}",
                duration
            )
            
            return has_cors
        except Exception as e:
            self.log_result("CORS headers", False, f"Error: {str(e)}")
            return False
    
    def test_response_time(self, endpoint: str = "/", samples: int = 10) -> bool:
        """性能基准 - 响应时间"""
        print("\n" + "="*60)
        print("TEST 5: Response Time Baseline")
        print("="*60)
        
        try:
            timings = []
            
            for i in range(samples):
                start = time.time()
                response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=TEST_TIMEOUT)
                duration = time.time() - start
                
                if response.status_code == 200:
                    timings.append(duration * 1000)  # 转换为毫秒
            
            if not timings:
                self.log_result("Response time baseline", False, "No successful requests")
                return False
            
            avg_time = statistics.mean(timings)
            min_time = min(timings)
            max_time = max(timings)
            stddev = statistics.stdev(timings) if len(timings) > 1 else 0
            
            self.performance_data["response_time"] = {
                "avg_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "stddev_ms": stddev,
                "samples": samples
            }
            
            message = f"Avg: {avg_time:.1f}ms, Min: {min_time:.1f}ms, Max: {max_time:.1f}ms"
            self.log_result("Response time baseline", True, message, avg_time)
            
            return True
        except Exception as e:
            self.log_result("Response time baseline", False, f"Error: {str(e)}")
            return False
    
    def test_concurrent_load(self, endpoint: str = "/", concurrent_users: int = 10, requests_per_user: int = 5) -> bool:
        """负载测试 - 并发请求"""
        print("\n" + "="*60)
        print("TEST 6: Concurrent Load Test")
        print("="*60)
        
        try:
            total_requests = concurrent_users * requests_per_user
            successful = 0
            failed = 0
            timings = []
            
            def make_request():
                try:
                    start = time.time()
                    response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=TEST_TIMEOUT)
                    duration = (time.time() - start) * 1000
                    
                    if response.status_code == 200:
                        return True, duration
                    else:
                        return False, None
                except:
                    return False, None
            
            start_total = time.time()
            with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
                futures = [executor.submit(make_request) for _ in range(total_requests)]
                
                for future in as_completed(futures):
                    success, duration = future.result()
                    if success:
                        successful += 1
                        timings.append(duration)
                    else:
                        failed += 1
            
            total_duration = time.time() - start_total
            
            if timings:
                avg_response = statistics.mean(timings)
                p95_response = sorted(timings)[int(len(timings) * 0.95)] if len(timings) > 1 else timings[0]
                throughput = total_requests / total_duration
                
                self.performance_data["concurrent_load"] = {
                    "concurrent_users": concurrent_users,
                    "total_requests": total_requests,
                    "successful": successful,
                    "failed": failed,
                    "success_rate": (successful / total_requests * 100),
                    "avg_response_ms": avg_response,
                    "p95_response_ms": p95_response,
                    "throughput_req_per_sec": throughput,
                    "total_duration_sec": total_duration
                }
                
                success_rate = successful / total_requests * 100
                message = f"Concurrent: {concurrent_users}, Success: {successful}/{total_requests} ({success_rate:.1f}%), Throughput: {throughput:.1f} req/s"
                passed = success_rate >= 95  # 95% 成功率阈值
                
                self.log_result("Concurrent load", passed, message, total_duration)
                return passed
            else:
                self.log_result("Concurrent load", False, "All requests failed")
                return False
        except Exception as e:
            self.log_result("Concurrent load", False, f"Error: {str(e)}")
            return False
    
    def test_security_headers(self) -> bool:
        """安全检查 - HTTP 安全头"""
        print("\n" + "="*60)
        print("TEST 7: Security Headers")
        print("="*60)
        
        try:
            response = requests.get(f"{API_BASE_URL}/", timeout=TEST_TIMEOUT)
            
            security_headers = {
                "x-content-type-options": "应该包含 nosniff",
                "x-frame-options": "应该包含 DENY 或 SAMEORIGIN",
                "x-xss-protection": "应该启用"
            }
            
            present_headers = {
                k: v in response.headers for k, v in security_headers.items()
            }
            
            has_minimum_headers = sum(present_headers.values()) >= 1  # 至少有一个
            
            message = f"Headers found: {sum(present_headers.values())}/3"
            self.log_result("Security headers", has_minimum_headers, message)
            
            return has_minimum_headers
        except Exception as e:
            self.log_result("Security headers", False, f"Error: {str(e)}")
            return False
    
    def test_input_validation(self) -> bool:
        """安全检查 - 输入验证"""
        print("\n" + "="*60)
        print("TEST 8: Input Validation")
        print("="*60)
        
        try:
            # 测试 SQL 注入
            start = time.time()
            response = requests.get(
                f"{API_BASE_URL}/api/user/list",
                params={"skip": "'; DROP TABLE users; --"},
                timeout=TEST_TIMEOUT
            )
            duration = time.time() - start
            
            # 应该返回 422 (参数验证错误) 或其他安全响应，而不是 500
            sql_injection_safe = response.status_code in [422, 400, 404, 200]  # 不应该是 500
            self.log_result(
                "SQL injection protection",
                sql_injection_safe,
                f"Status: {response.status_code}",
                duration
            )
            
            return sql_injection_safe
        except Exception as e:
            self.log_result("Input validation", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self) -> Tuple[int, int]:
        """运行所有测试"""
        print("\n" + "="*70)
        print("PRE系统 - 生产环境部署测试套件")
        print("="*70)
        print(f"API Base URL: {API_BASE_URL}")
        print(f"开始时间: {datetime.now().isoformat()}")
        
        # 检查连接
        try:
            requests.get(API_BASE_URL, timeout=5)
        except Exception as e:
            print(f"\n❌ 无法连接到 API: {str(e)}")
            print(f"请确保后端服务运行在 {API_BASE_URL}")
            return 0, 0
        
        # 运行测试
        self.test_api_availability()
        self.test_swagger_ui()
        self.test_error_handling()
        self.test_cors_headers()
        self.test_response_time()
        self.test_concurrent_load()
        self.test_security_headers()
        self.test_input_validation()
        
        # 汇总
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        
        passed = sum(1 for r in self.results if "✅" in r["status"])
        total = len(self.results)
        
        for result in self.results:
            print(f"{result['status']}: {result['test']} ({result['duration']:.3f}s)")
        
        print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        # 性能数据
        if self.performance_data:
            print("\n" + "-"*70)
            print("PERFORMANCE METRICS")
            print("-"*70)
            
            if "response_time" in self.performance_data:
                rt = self.performance_data["response_time"]
                print(f"\n响应时间基准:")
                print(f"  平均值: {rt['avg_ms']:.1f}ms")
                print(f"  最小值: {rt['min_ms']:.1f}ms")
                print(f"  最大值: {rt['max_ms']:.1f}ms")
                print(f"  标准差: {rt['stddev_ms']:.1f}ms")
                print(f"  采样数: {rt['samples']}")
            
            if "concurrent_load" in self.performance_data:
                cl = self.performance_data["concurrent_load"]
                print(f"\n并发负载测试:")
                print(f"  并发用户数: {cl['concurrent_users']}")
                print(f"  总请求数: {cl['total_requests']}")
                print(f"  成功/失败: {cl['successful']}/{cl['failed']}")
                print(f"  成功率: {cl['success_rate']:.1f}%")
                print(f"  平均响应时间: {cl['avg_response_ms']:.1f}ms")
                print(f"  P95 响应时间: {cl['p95_response_ms']:.1f}ms")
                print(f"  吞吐量: {cl['throughput_req_per_sec']:.1f} req/s")
                print(f"  总耗时: {cl['total_duration_sec']:.1f}s")
        
        print(f"\n完成时间: {datetime.now().isoformat()}")
        
        return passed, total


def main():
    """主函数"""
    suite = ProductionTestSuite()
    passed, total = suite.run_all_tests()
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
